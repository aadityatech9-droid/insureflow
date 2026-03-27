from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User,UserRole

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/auth/login")



def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db))->User:
    payload=decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired"
        )
    
    user_id_raw = payload.get("sub")

    if user_id_raw is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired"
        )

    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired",
        )
    
    user=db.query(User).filter(User.id==user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )   
    
    return user


def require_role(role:UserRole):
    def dependency(current_user:User=Depends(get_current_user))->User:
        if current_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    
    return dependency

