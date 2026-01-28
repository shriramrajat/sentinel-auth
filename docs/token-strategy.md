# 🎟️ Token Strategy (Rotation)

## Why Rotation?
To prevent token theft from being a permanent security risk.

## The Strategy
1.  **Storage**: 
    *   Access Tokens: Stateless (JWT).
    *   Refresh Tokens: Stateful (Stored in DB).
2.  **Usage**: 
    *   Refresh Token is **Single Use**.
    *   When used to get a new Access Token, the system **Revokes** the old Refresh Token and issues a new one.
3.  **Security**:
    *   If a thief steals a Refresh Token and uses it, the valid user will fail to use it later (or vice-versa).
    *   This anomaly allows detection (future feature).