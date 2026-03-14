from dataclasses import dataclass
from temporalio import activity
from lib.db import db_client
from .schemas import CreateAssessmentInput

@activity.defn(name="create_assessment")
async def create(input: CreateAssessmentInput) -> str:
    print(f"[ACTIVITY] create_assessment started with input: {input}")
    try:
        insert_data = {
            "school_id": input.school_id,
            "name": input.name
        }
        
        response = db_client.table("assessments").insert(insert_data).execute()
        
        print(f"[ACTIVITY] create_assessment DB response: {response.data}")
        assessment_id = response.data[0]['id']
        print(f"[ACTIVITY] create_assessment completed, assessment_id: {assessment_id}")
        return assessment_id
    except Exception as e:
        print(f"[ACTIVITY] create_assessment ERROR: {type(e).__name__}: {e}")
        raise
