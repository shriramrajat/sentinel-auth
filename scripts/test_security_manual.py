"""
Verify Security Layer.

This script tests:
1. Password hashing/verification
2. Token generation (access & refresh)
3. Token decoding and validation
"""

import sys
import os
import uuid
import time
from jose import jwt

# Add project root to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import get_password_hash, verify_password, decode_token
from app.core.tokens import create_access_token, create_refresh_token
from app.core.constants import TOKEN_TYPE_ACCESS, TOKEN_TYPE_REFRESH

def test_password_hashing():
    print("--- Testing Password Hashing ---")
    password = "secure_password_123"
    
    # Hash it
    hashed = get_password_hash(password)
    print(f"Password: {password}")
    print(f"Hashed:   {hashed[:20]}...")
    
    # Verify correct
    assert verify_password(password, hashed) == True
    print("✅ Password verification successful")
    
    # Verify wrong
    assert verify_password("wrong_password", hashed) == False
    print("✅ Wrong password rejected")


def test_tokens():
    print("\n--- Testing Tokens ---")
    user_id = str(uuid.uuid4())
    role = "admin"
    
    # 1. Access Token
    t0 = time.time()
    access_token = create_access_token(user_id, role)
    print(f"Access Token Generated: {access_token[:20]}...")
    
    # Decode
    payload = decode_token(access_token)
    print(f"Decoded Payload: {payload}")
    
    assert payload["sub"] == user_id
    assert payload["type"] == TOKEN_TYPE_ACCESS
    assert payload["role"] == role
    assert "exp" in payload
    print("✅ Access token verified")
    
    # 2. Refresh Token
    refresh_token = create_refresh_token(user_id)
    print(f"Refresh Token Generated: {refresh_token[:20]}...")
    
    # Decode
    payload_refresh = decode_token(refresh_token)
    print(f"Decoded Refresh Payload: {payload_refresh}")
    
    assert payload_refresh["sub"] == user_id
    assert payload_refresh["type"] == TOKEN_TYPE_REFRESH
    # Refresh token implies much longer expiry
    assert payload_refresh["exp"] > payload["exp"]
    print("✅ Refresh token verified")

def main():
    try:
        test_password_hashing()
        test_tokens()
        print("\n✨ All Security Tests Passed!")
    except Exception as e:
        print(f"\n❌ Tests Failed: {e}")
        raise

if __name__ == "__main__":
    main()
