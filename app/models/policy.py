from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SAEnum, func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class PolicyType(str,enum.Enum):
    health="health"
    life="life"
    vehicle="vehicle"
    property="property"


class Policy(Base):
    __tablename__="policies"
    id=Column(Integer,primary_key=True, autoincrement=True)
    name=Column(String(255),nullable=False)
    type=Column(SAEnum(PolicyType),nullable=False,index=True)
    premium=Column(Float,nullable=False)
    coverage_amount=Column(Float,nullable=False)
    duration_months=Column(Integer,nullable=False)
    description=Column(String(500),nullable=True)
    created_at=Column(DateTime,server_default=func.now())

    
    user_policies=relationship("UserPolicy", back_populates="policy")
    


