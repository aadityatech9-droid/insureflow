from sqlalchemy import Column,Integer,String,DateTime,Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base

class UserRole(str,enum.Enum):
    admin="admin"
    agent="agent"
    customer="customer"


class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True, autoincrement=True)
    email=Column(String(255),unique=True,nullable=False,index=True)
    password_hash=Column(String(255),nullable=False)
    role=Column(SAEnum(UserRole,name="userrole",create_type=False),default=UserRole.customer,nullable=False)
    created_at=Column(DateTime,server_default=func.now())
    updated_at=Column(DateTime,onupdate=func.now())

    user_policies=relationship("UserPolicy", back_populates="user")

    