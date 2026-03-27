from sqlalchemy import Column, Integer,Float,DateTime,ForeignKey,Enum as SAEnum 
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


from app.core.database import Base

class PolicyStatus(str,enum.Enum):
    active="active"
    expired="expired"
    cancelled="cancelled"



class UserPolicy(Base):
    __tablename__="user_policies"

    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"), index=True, nullable=False)
    policy_id=Column(Integer, ForeignKey("policies.id"), index=True, nullable=False)
    start_date=Column(DateTime,server_default=func.now())
    status=Column(
        SAEnum(PolicyStatus),
        default=PolicyStatus.active,
        nullable=False
    )

    premium_paid=Column(Float,default=0.0,nullable=False)

    user=relationship("User",back_populates="user_policies")
    policy=relationship("Policy",back_populates="user_policies")
    claims=relationship("Claim", back_populates="user_policy")      















