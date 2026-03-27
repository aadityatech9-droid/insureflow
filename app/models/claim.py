from sqlalchemy import Column, Integer,DateTime,func, Float,String,DateTime, ForeignKey,Enum as SAEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class ClaimStatus(str,enum.Enum):
    pending="pending"
    approved="approved"
    rejected="rejected"

class Claim(Base):
    __tablename__="claims"

    id=Column(Integer,primary_key=True,index=True)
    user_policy_id=Column(
        Integer,
        ForeignKey("user_policies.id"),
        index=True,
        nullable=False
    )

    amount=Column(Float,nullable=False)
    reason=Column(String(500),nullable=False)

    status=Column(
        SAEnum(ClaimStatus),
        default=ClaimStatus.pending,
        index=True,
        nullable=False
    )
    filed_at=Column(DateTime,server_default=func.now())
    resolved_at=Column(DateTime,nullable=True)

    user_policy=relationship("UserPolicy",back_populates="claims")



