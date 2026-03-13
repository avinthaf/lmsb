import os
from jose import jwt, jwk
from jose.exceptions import JWTError
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

def get_jwks() -> Dict[str, Any]:
    """Fetch the JWKS from Supabase"""
    supabase_url = os.environ.get("SUPABASE_URL")
    if not supabase_url:
        raise ValueError("SUPABASE_URL environment variable not set")
    
    jwks_url = f"{supabase_url}/auth/v1/.well-known/jwks.json"
    response = requests.get(jwks_url)
    response.raise_for_status()
    return response.json()

def verify_jwt(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a Supabase JWT and return the decoded payload.
    
    Args:
        token: The JWT token (without "Bearer " prefix)
        
    Returns:
        The decoded payload if valid, None if invalid
    """
    try:
        print(f"[DEBUG] Verifying token: {token[:20]}...")
        
        # Decode header to get algorithm and key ID
        header = jwt.get_unverified_header(token)
        print(f"[DEBUG] JWT header: {header}")
        alg = header.get('alg')
        kid = header.get('kid')
        
        if not kid:
            print("[DEBUG] No kid found in header")
            return None
            
        # Get JWKS and find the matching key
        print(f"[DEBUG] Fetching JWKS...")
        jwks = get_jwks()
        print(f"[DEBUG] JWKS keys: {[k.get('kid') for k in jwks.get('keys', [])]}")
        
        key = None
        for jwk_key in jwks['keys']:
            if jwk_key['kid'] == kid:
                key = jwk_key
                break
                
        if not key:
            print(f"[DEBUG] No matching key found for kid: {kid}")
            return None
            
        print(f"[DEBUG] Found matching key for algorithm: {alg}")
        
        # Convert JWK to public key for verification
        public_key = jwk.construct(key)
        
        # Verify and decode the token
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[alg],
            audience="authenticated"
        )
        
        print(f"[DEBUG] Token verified successfully. Email: {payload.get('email')}")
        return payload
        
    except (JWTError, requests.RequestException, ValueError, KeyError) as e:
        print(f"[DEBUG] JWT verification error: {type(e).__name__}: {e}")
        return None

def get_user_id_from_token(bearer_token: str) -> Optional[str]:
    """
    Extract user ID from a bearer token.
    
    Args:
        bearer_token: The full bearer token (e.g., "Bearer eyJhbGciOi...")
        
    Returns:
        The user's ID (sub claim) if valid, None if invalid
    """
    # Remove "Bearer " prefix if present
    token = bearer_token.replace("Bearer ", "").strip()
    
    if not token:
        return None
        
    payload = verify_jwt(token)
    if payload and 'sub' in payload:
        return payload['sub']
        
    return None