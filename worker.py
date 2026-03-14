import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from workflows import (
        CreatePlatformUserWorkflow,
        CreateOrganizationWorkflow,
        CreateCourseWorkflow,
        CreateCourseContentWorkflow,
        DeleteCourseContentWorkflow,
        DeleteCourseSectionWorkflow
    )
    from platform_users import activities
    from organizations import activities as org_activities
    from courses import activities as course_activities
    from assessments import activities as assessment_activities

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="main",
        workflows=[
            CreatePlatformUserWorkflow,
            CreateOrganizationWorkflow,
            CreateCourseWorkflow,
            CreateCourseContentWorkflow,
            DeleteCourseContentWorkflow,
            DeleteCourseSectionWorkflow,
        ],
        activities=[
            activities.create,
            org_activities.create,
            org_activities.create_member,
            course_activities.create,
            course_activities.create_author,
            course_activities.create_section,
            course_activities.create_content,
            course_activities.link_content_to_section,
            course_activities.delete_content,
            course_activities.delete_content_links,
            course_activities.update_content_ref_id,
            course_activities.delete_section,
            course_activities.delete_section_content_links,
            assessment_activities.create,
        ],
    )
    print("Worker started, listening on task queue: main")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())