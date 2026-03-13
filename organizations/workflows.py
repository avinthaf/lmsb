from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from organizations.schemas import CreateOrganizationInput, CreateOrganizationMemberInput

@workflow.defn(name="CreateOrganizationWorkflow")
class CreateOrganizationWorkflow:
    @workflow.run
    async def run(self, user_id: str, org_name: str, role_id: str) -> str:
        # Step 1: Create the organization
        org_input = CreateOrganizationInput(name=org_name)
        org_result = await workflow.execute_activity(
            "create_organization",
            org_input,
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        # Step 2: Create the organization member with the returned org_id
        member_input = CreateOrganizationMemberInput(
            organization_id=org_result,
            user_id=user_id,
            role_id=role_id
        )
        member_result = await workflow.execute_activity(
            "create_organization_member",
            member_input,
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        return f"Created organization {org_result} with member {user_id}"