from dataclasses import dataclass
from temporalio import activity
from db import db_client
from models import Role

# Get all roles
@activity.defn(name="get_roles")
async def get() -> list[Role]:
    response = (
        db_client.table("roles")
        .select("*")
        .execute()
    )
    return [Role(**role) for role in response.data]