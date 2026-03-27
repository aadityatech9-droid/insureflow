from pydantic import BaseModel
from app.models.policy import PolicyType

from datetime import datetime
from typing import Optional

class PolicyCreate(BaseModel):
    name:str
    type:PolicyType
    premium:float
    coverage_amount:float
    duration_months:int
    description:Optional[str]=None


class PolicyResponse(BaseModel):
    id:int
    name:str
    type:PolicyType
    premium:float
    coverage_amount:float
    duration_months:int
    decription:Optional[str]=None
    created_at:datetime

    model_config={
        "from_attributes":True
    }