from sqlalchemy.orm import Session
from fastapi import HTTPException, status


from app.models.user import User
from app.schemas.auth import RegisterRequest,LoginRequest
from app.core.security import hash_password,verify_password,create_access_token,create_refresh_token



def register_user(db:Session,data:RegisterRequest)->User:
    existing_user=db.query(User).filter(User.email==data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user=User(
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db:Session,data:LoginRequest)->dict:
    user=db.query(User).filter(User.email==data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credential"

        )
    
    if not verify_password(data.password,user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token_data={
        "sub":str(user.id),
        "email":user.email,
        "role":user.role
    }

    access_token=create_access_token(token_data)
    refresh_token=create_refresh_token(token_data)

    return{
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
    }