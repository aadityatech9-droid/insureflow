from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from app.core.database import get_db
from app.schemas.auth import RegisterRequest,LoginRequest,TokenResponse,UserResponse
from app.services import auth_services
from app.core.dependencies import get_current_user


router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=UserResponse,status_code=201)
def register(data:RegisterRequest,db:Session=Depends(get_db)):
    user=auth_services.register_user(db,data)
    return user



@router.post("/login",response_model=TokenResponse)
def login(data:LoginRequest,db:Session=Depends(get_db)):
    
    tokens=auth_services.login_user(db,data)
    return tokens


@router.get("/me")
def get_me(user=Depends(get_current_user)):
    return user