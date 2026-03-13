import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from workflows import CreatePlatformUserWorkflow, CreateOrganizationWorkflow
    from courses.workflows import CreateCourseWorkflow
    from platform_users import activities
    from organizations import activities as org_activities
    from courses import activities as course_activities

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="main",
        workflows=[
            CreatePlatformUserWorkflow,
            CreateOrganizationWorkflow,
            CreateCourseWorkflow,
        ],
        activities=[
            activities.create,
            org_activities.create,
            org_activities.create_member,
            course_activities.create,
            course_activities.create_author,
        ],
    )
    print("Worker started, listening on task queue: main")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())