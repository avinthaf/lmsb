from dataclasses import dataclass
from uuid import UUID
from temporalio import activity
from lib import db_client
from .schemas import CreatePlatformUserInput, GetPlatformUserInput

@activity.defn(name="create_platform_user")
async def create(input: CreatePlatformUserInput) -> str:
    response = (
        db_client.table("platform_users")
        .insert({"id": str(input.id), "email": input.email})
        .execute()
    )
    return f"Created user: {input.email}"

@activity.defn(name="get_platform_user_by_email")
async def get(input: GetPlatformUserInput) -> str:
    response = (
        db_client.table("platform_users")
        .select("*")
        .limit(1)
        .single()
        .execute()
    )
    return response.data