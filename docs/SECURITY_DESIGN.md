# 🔐 Security Architecture Deep Dive

## 🧠 Core Design Principles (Q&A)

### 1. Why is the Access Token short-lived (15 mins)?
**Answer:** To minimize the damage window in case of token theft.
- Since Access Tokens are often stored in frontend memory or localStorage and sent with every request, they are susceptible to XSS attacks or interception.
- If stolen, an attacker can only use it for a few minutes.
- Because it is **stateless** (not checked against DB for every request to save performance), we can't revoke it easily. Short expiry is the only efficient way to limit its validity.

### 2. Why is the Refresh Token long-lived (7 days)?
**Answer:** To provide a good User Experience (UX) while maintaining security.
- Users shouldn't have to log in every 15 minutes.
- The Refresh Token is kept more securely (e.g., HTTPOnly cookie) and only sent to the `/auth/refresh` endpoint, reducing exposure.
- Its long life allows the user to stay "logged in" for days.

### 3. Why is the Refresh Token stored in DB but Access Token is not?
**Answer:** To allow **Revocation**.
- **Access Tokens**: Designed for speed. Validated mathematically (signature) without DB lookups. If we stored them, we'd lose the performance benefit of JWTs.
- **Refresh Tokens**: Designed for control. When a user logs out or changes their password, we **must** be able to kill the session immediately.
- By checking the Refresh Token against the DB during the refresh flow, we can check if `is_revoked=True` or if the parent User is deleted/blocked. This gives us a "Kill Switch" for sessions without checking DB on every API call.
- We strictly store the **hash** of the refresh token (not the raw token) so even a DB leak doesn't compromise active user sessions.

---

## 🏗️ Implementation Details

### **1. Token Separation** (`app/core/tokens.py`)
We explicitly separate creation logic:
- `create_access_token()`: Sets `type="access"` and 15m expiry.
- `create_refresh_token()`: Sets `type="refresh"` and 7d expiry.

### **2. Payload Structure**
All tokens contain:
- `sub`: User UUID (Target)
- `type`: Token purpose (Critical for preventing misuse of access token as refresh token)
- `exp`: Expiration time
- `iat`: Issued at time

### **3. Cryptography**
- **Algorithm**: HS256 (HMAC SHA-256)
- **Library**: `python-jose` with `cryptography` backend for speed and security.
- **Password Hashing**: Bcrypt via `passlib` (Work factor auto-calibrated).

---

## 🔄 The Authentication Loop

1. **Login**: Client sends Creds → Server returns Access (15m) + Refresh (7d).
2. **Access**: Client sends Access Token → Server verifies signature (No DB).
3. **Expire**: Access Token expires (401 Error).
4. **Refresh**: Client sends Refresh Token → Server:
   - Verifies Signature
   - **Checks DB**: Is hash present? Is `is_revoked`? Is User active?
   - If OK: Issues NEW Access + NEW Refresh (Rotation).
   - Revokes OLD Refresh.

This Hybrid approach gives us the **Speed of stateless JWTs** + **Control of stateful sessions**.
