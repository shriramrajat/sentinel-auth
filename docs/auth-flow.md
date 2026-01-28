# 🔐 Authentication Flow

## 1. Registration (`/signup`)
1. User submits email/password.
2. System checks for duplicates.
3. System hashes password using **Bcrypt**.
4. User created with default role [user](cci:1://file:///d:/Rajat/Projects/SentinelAuth/SentinelAuth/app/services/user_service.py:63:4-83:59).

## 2. Login (`/login`)
1. User submits credentials.
2. System verifies hash.
3. System issues **Pair of Tokens**:
   *   [access_token](cci:1://file:///d:/Rajat/Projects/SentinelAuth/SentinelAuth/app/services/auth_service.py:54:4-112:9): Short-lived (15 min). Used for API access.
   *   [refresh_token](cci:1://file:///d:/Rajat/Projects/SentinelAuth/SentinelAuth/app/api/routes/auth.py:22:0-28:67): Long-lived (7 days). Stored in DB (hashed).

## 3. Secure Access
*   Client sends `Authorization: Bearer <access_token>`.
*   Server verifies JWT signature and expiration.