"""Auth utilities: password hashing, JWT tokens, email verification."""
import hashlib
import hmac
import os
import re
import secrets
from datetime import datetime, timezone
from functools import wraps

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
from flask import current_app, request, jsonify

from app.extensions import db

_ph = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16,
)


# ── Password ──────────────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    return _ph.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return _ph.verify(hashed, plain)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def password_needs_rehash(hashed: str) -> bool:
    return _ph.check_needs_rehash(hashed)


_PASSWORD_RE = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
)


def validate_password_strength(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, 'Password must be at least 8 characters.'
    if not _PASSWORD_RE.match(password):
        return False, 'Password must contain uppercase, lowercase, and a digit.'
    return True, ''


# ── JWT tokens ────────────────────────────────────────────────────────────────

def _utcnow():
    return datetime.now(timezone.utc)


def create_access_token(user_id: int) -> str:
    payload = {
        'sub': str(user_id),
        'type': 'access',
        'iat': _utcnow(),
        'exp': _utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')


def create_refresh_token_value() -> str:
    """Return a cryptographically random opaque token (not JWT)."""
    return secrets.token_urlsafe(64)


def hash_token(token: str) -> str:
    """Store only the hash of refresh tokens in the DB."""
    return hashlib.sha256(token.encode()).hexdigest()


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        current_app.config['JWT_SECRET_KEY'],
        algorithms=['HS256'],
        options={'require': ['sub', 'exp', 'type']},
    )


# ── Email verification ────────────────────────────────────────────────────────

def generate_verification_token() -> str:
    return secrets.token_urlsafe(48)


def send_verification_email(user, token: str):
    """Send verification email. Logs to console in dev if mail not configured."""
    verify_url = (
        f"{current_app.config['FRONTEND_URL']}/verify-email?token={token}"
    )
    mail_user = current_app.config.get('MAIL_USERNAME')
    if not mail_user:
        current_app.logger.info(
            f'[DEV] Verification link for {user.email}: {verify_url}'
        )
        return

    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Verify your Nova Health email'
        msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
        msg['To'] = user.email

        html = f"""
        <html><body>
        <p>Hi {user.name or 'there'},</p>
        <p>Click below to verify your email (link expires in 24 hours):</p>
        <p><a href="{verify_url}">{verify_url}</a></p>
        <p>If you didn't create an account, ignore this email.</p>
        </body></html>
        """
        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as smtp:
            smtp.starttls()
            smtp.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            smtp.send_message(msg)
    except Exception as e:
        current_app.logger.error(f'Failed to send verification email: {e}')


# ── Request helpers ───────────────────────────────────────────────────────────

def get_client_ip() -> str:
    forwarded = request.headers.get('X-Forwarded-For')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.remote_addr or 'unknown'


def get_user_agent() -> str:
    return (request.headers.get('User-Agent') or '')[:512]


# ── Auth decorator ────────────────────────────────────────────────────────────

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid Authorization header.'}), 401
        token = auth_header[7:]
        try:
            payload = decode_access_token(token)
            if payload.get('type') != 'access':
                raise ValueError('Wrong token type')
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Access token expired.'}), 401
        except Exception:
            return jsonify({'error': 'Invalid access token.'}), 401

        from app.models.user import User
        user = db.session.get(User, int(payload['sub']))
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive.'}), 401

        request.current_user = user
        return f(*args, **kwargs)
    return decorated
