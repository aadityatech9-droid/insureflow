from fastapi import status
from pydantic import BaseModel
from app.models import user_policy
from app.models.claim import ClaimStatus
from datetime import datetime


class claimCreate(BaseModel):
    user_policy_id:int
    amount:float
    reason:str

class claimResponse(BaseModel):
    id:int
    user_policy_id:int
    amount:float
    reason:str
    status:ClaimStatus
    filed_at:datetime

    model_config={
        "from_attributes":True
    }
