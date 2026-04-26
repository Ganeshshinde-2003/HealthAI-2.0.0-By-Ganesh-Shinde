"""Auth routes: signup, login, logout, refresh, verify-email, me."""
import re
from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request, current_app

from app.extensions import db, limiter
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.login_attempt import LoginAttempt
from app.utils.auth import (
    hash_password,
    verify_password,
    password_needs_rehash,
    validate_password_strength,
    create_access_token,
    create_refresh_token_value,
    hash_token,
    decode_access_token,
    generate_verification_token,
    send_verification_email,
    get_client_ip,
    get_user_agent,
    require_auth,
)

auth_bp = Blueprint('auth', __name__)

_EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

REFRESH_COOKIE = 'refresh_token'


def _set_refresh_cookie(response, token_value: str, expires: datetime):
    response.set_cookie(
        REFRESH_COOKIE,
        token_value,
        httponly=True,
        secure=True,
        samesite='Lax',
        expires=expires,
        path='/api/auth',
    )
    return response


def _clear_refresh_cookie(response):
    response.delete_cookie(REFRESH_COOKIE, path='/api/auth')
    return response


def _log_attempt(user_id, email: str, success: bool):
    attempt = LoginAttempt(
        user_id=user_id,
        email=email,
        ip_address=get_client_ip(),
        user_agent=get_user_agent(),
        success=success,
    )
    db.session.add(attempt)


# ── Signup ────────────────────────────────────────────────────────────────────

@auth_bp.route('/signup', methods=['POST'])
@limiter.limit('3 per hour', key_func=get_client_ip)
def signup():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    name = (data.get('name') or '').strip()

    # Validate inputs
    if not email or not _EMAIL_RE.match(email):
        return jsonify({'error': 'Valid email is required.'}), 400
    if not name:
        return jsonify({'error': 'Name is required.'}), 400

    ok, msg = validate_password_strength(password)
    if not ok:
        return jsonify({'error': msg}), 400

    if User.query.filter_by(email=email).first():
        # Don't reveal existence — return same response
        return jsonify({'message': 'If that email is new, a verification link has been sent.'}), 201

    verification_token = generate_verification_token()
    expires = datetime.now(timezone.utc) + timedelta(
        hours=current_app.config['EMAIL_VERIFICATION_EXPIRES_HOURS']
    )

    user = User(
        email=email,
        name=name,
        password_hash=hash_password(password),
        email_verified=False,
        email_verification_token=verification_token,
        verification_token_expires=expires,
    )
    db.session.add(user)
    db.session.commit()

    send_verification_email(user, verification_token)

    return jsonify({'message': 'If that email is new, a verification link has been sent.'}), 201


# ── Verify email ──────────────────────────────────────────────────────────────

@auth_bp.route('/verify-email', methods=['GET'])
@limiter.limit('10 per hour', key_func=get_client_ip)
def verify_email():
    token = request.args.get('token', '').strip()
    if not token:
        return jsonify({'error': 'Verification token is required.'}), 400

    user = User.query.filter_by(email_verification_token=token).first()
    now = datetime.now(timezone.utc)

    if not user:
        return jsonify({'error': 'Invalid or expired token.'}), 400

    token_expires = user.verification_token_expires
    if token_expires and token_expires.tzinfo is None:
        token_expires = token_expires.replace(tzinfo=timezone.utc)

    if not token_expires or token_expires < now:
        return jsonify({'error': 'Invalid or expired token.'}), 400

    user.email_verified = True
    user.email_verification_token = None
    user.verification_token_expires = None
    db.session.commit()

    return jsonify({'message': 'Email verified successfully. You can now log in.'}), 200


# ── Login ─────────────────────────────────────────────────────────────────────

@auth_bp.route('/login', methods=['POST'])
@limiter.limit('5 per minute', key_func=get_client_ip)
@limiter.limit('20 per hour', key_func=get_client_ip)
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()

    # Account lockout check
    if user and user.is_locked():
        _log_attempt(user.id, email, False)
        db.session.commit()
        return jsonify({'error': 'Account is temporarily locked. Try again later.'}), 429

    # Constant-time-ish: always verify even if user not found
    dummy = '$argon2id$v=19$m=65536,t=3,p=2$dummysaltvalue1234567890$dummyhashvalue1234567890123456'
    stored_hash = user.password_hash if user else dummy
    valid = verify_password(password, stored_hash)

    if not user or not valid:
        if user:
            user.failed_login_attempts += 1
            max_attempts = current_app.config['MAX_LOGIN_ATTEMPTS']
            if user.failed_login_attempts >= max_attempts:
                lockout_mins = current_app.config['ACCOUNT_LOCKOUT_MINUTES']
                user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=lockout_mins)
            _log_attempt(user.id, email, False)
        else:
            _log_attempt(None, email, False)
        db.session.commit()
        return jsonify({'error': 'Invalid email or password.'}), 401

    if not user.email_verified:
        _log_attempt(user.id, email, False)
        db.session.commit()
        return jsonify({'error': 'Please verify your email before logging in.'}), 403

    # Successful login — reset lockout counters
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login = datetime.now(timezone.utc)

    if password_needs_rehash(user.password_hash):
        user.password_hash = hash_password(password)

    # Issue tokens
    access_token = create_access_token(user.id)
    refresh_value = create_refresh_token_value()
    refresh_expires = datetime.now(timezone.utc) + current_app.config['JWT_REFRESH_TOKEN_EXPIRES']

    rt = RefreshToken(
        user_id=user.id,
        token_hash=hash_token(refresh_value),
        expires_at=refresh_expires,
        ip_address=get_client_ip(),
        user_agent=get_user_agent(),
    )
    db.session.add(rt)
    _log_attempt(user.id, email, True)
    db.session.commit()

    resp = jsonify({
        'access_token': access_token,
        'user': user.to_dict(),
    })
    return _set_refresh_cookie(resp, refresh_value, refresh_expires)


# ── Refresh ───────────────────────────────────────────────────────────────────

@auth_bp.route('/refresh', methods=['POST'])
@limiter.limit('30 per hour', key_func=get_client_ip)
def refresh():
    refresh_value = request.cookies.get(REFRESH_COOKIE)
    if not refresh_value:
        return jsonify({'error': 'No refresh token provided.'}), 401

    token_hash = hash_token(refresh_value)
    rt = RefreshToken.query.filter_by(token_hash=token_hash).first()

    if not rt or not rt.is_valid():
        resp = jsonify({'error': 'Invalid or expired refresh token.'})
        return _clear_refresh_cookie(resp), 401

    user = db.session.get(User, rt.user_id)
    if not user or not user.is_active:
        resp = jsonify({'error': 'User not found.'})
        return _clear_refresh_cookie(resp), 401

    # Rotate: revoke old, issue new
    rt.revoked = True

    new_refresh_value = create_refresh_token_value()
    new_expires = datetime.now(timezone.utc) + current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
    new_rt = RefreshToken(
        user_id=user.id,
        token_hash=hash_token(new_refresh_value),
        expires_at=new_expires,
        ip_address=get_client_ip(),
        user_agent=get_user_agent(),
    )
    db.session.add(new_rt)
    db.session.commit()

    access_token = create_access_token(user.id)
    resp = jsonify({'access_token': access_token})
    return _set_refresh_cookie(resp, new_refresh_value, new_expires)


# ── Logout ────────────────────────────────────────────────────────────────────

@auth_bp.route('/logout', methods=['POST'])
def logout():
    refresh_value = request.cookies.get(REFRESH_COOKIE)
    if refresh_value:
        token_hash = hash_token(refresh_value)
        rt = RefreshToken.query.filter_by(token_hash=token_hash).first()
        if rt:
            rt.revoked = True
            db.session.commit()

    resp = jsonify({'message': 'Logged out successfully.'})
    return _clear_refresh_cookie(resp)


# ── Me ────────────────────────────────────────────────────────────────────────

@auth_bp.route('/me', methods=['GET'])
@require_auth
def me():
    return jsonify({'user': request.current_user.to_dict()})
