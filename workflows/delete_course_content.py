from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from courses.schemas import DeleteCourseContentInput

@workflow.defn(name="DeleteCourseContentWorkflow")
class DeleteCourseContentWorkflow:
    @workflow.run
    async def run(self, content_id: str) -> str:
        # Step 1: Soft delete the course content
        delete_input = DeleteCourseContentInput(
            content_id=content_id
        )
        await workflow.execute_activity(
            "delete_course_content",
            delete_input,
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        # Step 2: Soft delete all junction table records linking to this content
        await workflow.execute_activity(
            "delete_course_content_links",
            delete_input,
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        return f"Deleted course content {content_id} and all associated links"
