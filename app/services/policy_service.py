import json
from sqlalchemy.orm import Session
from app.models.policy import Policy
from app.schemas.policy import PolicyCreate,PolicyResponse
from app.core.redis import redis_client

CACHE_KEY="all_policies"
CACHE_TTL=300

def get_all_policies(db:Session):

    try:

        cached=redis_client.get(CACHE_KEY)
        if cached:
            print("CACHE HIT") 
            return json.loads(cached)
    except Exception as e :
        print("reddis read failed",e)
    
    print("CACHE MISS → DB")
    policies=db.query(Policy).all()

    data=[
        PolicyResponse.model_validate(policy).model_dump(mode="json")
        for policy in policies

    ]
    try:

        redis_client.setex(CACHE_KEY,CACHE_TTL,json.dumps(data))
        print("CACHE SET")
    except Exception as e:
        print("reddis write failed")
    return data


def create_policy(db:Session,data:PolicyCreate)->Policy:
     policy=Policy(**data.model_dump())
     db.add(policy)
     db.commit()
     db.refresh(policy)
     redis_client.delete(CACHE_KEY)
     return policy
