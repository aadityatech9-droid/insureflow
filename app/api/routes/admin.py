from fastapi import APIRouter,Depends
from app.core.dependencies import require_role
from app.models.user import UserRole,User

router= APIRouter(prefix="/admin",tags=['Admin'])


@router.get("/users")
def get_users(admin:User=Depends(require_role(UserRole.admin))):
    return {"message":"hello admin"}


@router.get("/dashboard")
def get_dashboard(agent:User=Depends(require_role(UserRole.agent))):
    return {"message":"hello agent"}


