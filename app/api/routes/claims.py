from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from typing import List


from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.claim import claimCreate,claimResponse
from app.services import claim_service


router=APIRouter(prefix="/claims",tags=['claims'])

@router.post('/',response_model=claimResponse,status_code=status.HTTP_201_CREATED)
def file_claim(data:claimCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return claim_service.file_claim(db,data,current_user)

@router.get("/my",response_model=List[claimResponse])
def  get_my_claims(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return claim_service.get_my_claims(db,current_user)

