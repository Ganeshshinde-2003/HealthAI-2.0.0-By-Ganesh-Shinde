# Auth Implementation Tracker

## Overview
High-security email + password authentication for Nova Health backend.

---

## Status

| Task | Status | Notes |
|------|--------|-------|
| Install dependencies | ✅ Done | argon2-cffi, PyJWT, Flask-Limiter |
| Update requirements.txt | ✅ Done | |
| Update User model | ✅ Done | Added password_hash, email_verified, verification fields |
| Create RefreshToken model | ✅ Done | |
| Create LoginAttempt model | ✅ Done | |
| Update config | ✅ Done | JWT settings, rate limit settings |
| Auth utilities (password, JWT) | ✅ Done | |
| Auth routes blueprint | ✅ Done | signup, login, logout, refresh, verify-email |
| Register blueprint in app | ✅ Done | |
| Alembic migration | ⏳ Pending | Run manually — see commands below |
| Auth API layer (authApi.ts) | ✅ Done | |
| Auth context (AuthContext.tsx) | ✅ Done | Access token in memory, refresh cookie |
| Frontend login page | ✅ Done | /login |
| Frontend signup page | ✅ Done | /signup — with live password strength checker |

---

## Endpoints

| Method | Route | Description | Auth Required |
|--------|-------|-------------|---------------|
| POST | `/api/auth/signup` | Register new user | No |
| POST | `/api/auth/login` | Login, get tokens | No |
| POST | `/api/auth/logout` | Revoke refresh token | Yes (Bearer) |
| POST | `/api/auth/refresh` | Rotate refresh token | No (cookie) |
| GET | `/api/auth/verify-email` | Verify email address | No (token param) |
| GET | `/api/auth/me` | Get current user | Yes (Bearer) |

---

## Security Measures Implemented

- **Argon2id** password hashing (memory-hard, side-channel resistant)
- **Short-lived JWT access tokens** (15 min expiry)
- **Refresh token rotation** (7 day expiry, HttpOnly cookie, single-use)
- **Refresh token revocation** on logout (stored + invalidated in DB)
- **Rate limiting**: 5 login attempts / minute per IP, 3 signups / hour per IP
- **Account lockout**: 30 min lock after 10 failed login attempts
- **Login attempt logging**: IP, timestamp, user-agent, success/failure
- **Email verification**: HMAC-signed, time-limited (24h), single-use token
- **Input validation**: Email format, password complexity (8+ chars, upper, lower, digit)
- **Secure headers**: Applied via Flask-Limiter + response middleware
- **Secrets via .env**: JWT secret, DB URL — never hardcoded

---

## New Environment Variables Required

Add these to your `.env` file:

```env
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this
JWT_REFRESH_SECRET_KEY=your-refresh-secret-key-change-this
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@novahealth.com
FRONTEND_URL=http://localhost:3000
```

---

## DB Tables Added

- `users` — extended with `password_hash`, `email_verified`, `email_verification_token`, `verification_token_expires`, `failed_login_attempts`, `locked_until`
- `refresh_tokens` — `id`, `user_id`, `token_hash`, `expires_at`, `revoked`, `created_at`, `ip_address`, `user_agent`
- `login_attempts` — `id`, `user_id` (nullable), `email`, `ip_address`, `user_agent`, `success`, `created_at`

---

## How to Run Migration

```bash
cd backend
alembic revision --autogenerate -m "add auth tables"
alembic upgrade head
```
