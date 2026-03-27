from app.core.celery import celery_app

@celery_app.task
def process_claim_submission(claim_id:int,user_email:str,policy_name:str):
    print(f'Sending email to {user_email}')
    print(f'generating pdf  for claim{claim_id}')
    print(f'Notifying agent for claim{claim_id}')

    return {
        "status":"processed",
        "claim_id":claim_id
    }

@celery_app.task
def update_claim_status(claim_id:int,new_status:str,user_email:str):
    print(f"claim {claim_id} status updated to {new_status}")
    print(f'Notifying{user_email} of status change')

    return {
       "status":"notified",
       "claim_id":claim_id
    }