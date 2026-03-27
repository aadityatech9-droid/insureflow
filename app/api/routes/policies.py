from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user,require_role
from app.models.user import UserRole
from app.schemas.policy import PolicyCreate,PolicyResponse
from app.services import policy_service

router=APIRouter(prefix="/policies",tags=["Policies"])


@router.get("/",response_model=list[PolicyResponse])
def get_policies(db:Session=Depends(get_db),user=Depends(get_current_user)):
    return policy_service.get_all_policies(db)


@router.post("/",response_model=PolicyResponse,status_code=status.HTTP_201_CREATED)
def create_policy(data:PolicyCreate,db:Session=Depends(get_db),user=Depends(require_role(UserRole.admin))):
    return policy_service.create_policy(db,data)    