from datetime import datetime ,timedelta 
from jose import JWTError,jwt
from passlib.context import CryptContext
from fastapi import HTTPException,status
from app.core.config import settings


# bcrypt has a 72-byte password limit; bcrypt_sha256 pre-hashes to avoid that.
# Keep "bcrypt" in the list so existing hashes continue to verify.
pwd_context=CryptContext(schemes=["bcrypt_sha256", "bcrypt"],deprecated="auto")


def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        # bcrypt raises when password > 72 bytes; treat as non-match
        return False



def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp":expire,
        "type":"access"
    })
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)


def create_refresh_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp":expire,
        "type":"refresh"
    })
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)


def decode_token(token:str):
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )




