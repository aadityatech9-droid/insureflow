from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.models.claim import Claim,ClaimStatus
from app.models.user import User
from app.models.user_policy import UserPolicy
from app.schemas.claim import claimCreate
from app.tasks.claim_tasks import process_claim_submission

def file_claim(db: Session,data:claimCreate,current_user):
    user_policy=db.query(UserPolicy).filter(
        UserPolicy.id==data.user_policy_id).first()
    
    if not user_policy or user_policy.user_id!=current_user.id:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    claim=Claim(
        user_policy_id=data.user_policy_id,
        amount=data.amount,
        reason=data.reason,
        status=ClaimStatus.pending
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)
    
    process_claim_submission.delay(
        claim_id=claim.id,
        user_email=current_user.email,
        policy_name=user_policy.policy.name
    )
    return claim

def get_my_claims(db:Session,current_user):
    claims=(
        db.query(Claim)
        .join(UserPolicy,Claim.user_policy_id==UserPolicy.id)
        .filter(UserPolicy.user_id==current_user.id)
        .all()

    )
    return claims
