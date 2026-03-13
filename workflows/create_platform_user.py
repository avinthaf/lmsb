from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from platform_users.schemas import CreatePlatformUserInput

@workflow.defn(name="CreatePlatformUserWorkflow")
class CreatePlatformUserWorkflow:
    @workflow.run
    async def run(self, input: CreatePlatformUserInput) -> str:
        return await workflow.execute_activity(
            "create_platform_user",
            input,
            start_to_close_timeout=timedelta(seconds=10),
        )
