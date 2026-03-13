from dataclasses import dataclass
from temporalio import activity
from lib.db import db_client
from .schemas import CreateOrganizationInput, CreateOrganizationMemberInput     

@activity.defn(name="create_organization")
async def create(input: CreateOrganizationInput) -> str:
    print(f"[ACTIVITY] create_organization started with input: {input}")
    try:
        response = (
            db_client.table("organizations")
            .insert({"name": input.name})
            .execute()
        )
        print(f"[ACTIVITY] create_organization DB response: {response.data}")
        # Return the organization ID from the created record
        org_id = response.data[0]['id']
        print(f"[ACTIVITY] create_organization completed, org_id: {org_id}")
        return org_id
    except Exception as e:
        print(f"[ACTIVITY] create_organization ERROR: {type(e).__name__}: {e}")
        raise

@activity.defn(name="create_organization_member")
async def create_member(input: CreateOrganizationMemberInput) -> str:
    print(f"[ACTIVITY] create_organization_member started with input: {input}")
    try:
        response = (
            db_client.table("organization_members")
            .insert({"organization_id": input.organization_id, "user_id": input.user_id, "role_id": input.role_id})
            .execute()
        )
        print(f"[ACTIVITY] create_organization_member DB response: {response.data}")
        result = f"Created organization member: {input.user_id}"
        print(f"[ACTIVITY] create_organization_member completed: {result}")
        return result
    except Exception as e:
        print(f"[ACTIVITY] create_organization_member ERROR: {type(e).__name__}: {e}")
        raise