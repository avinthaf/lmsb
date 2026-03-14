from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from courses.schemas import DeleteCourseSectionInput

@workflow.defn(name="DeleteCourseSectionWorkflow")
class DeleteCourseSectionWorkflow:
    @workflow.run
    async def run(self, section_id: str) -> str:
        # Step 1: Soft delete the course section
        delete_input = DeleteCourseSectionInput(
            section_id=section_id
        )
        await workflow.execute_activity(
            "delete_course_section",
            delete_input,
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        # Step 2: Soft delete all junction table records linking to this section
        await workflow.execute_activity(
            "delete_course_section_content_links",
            delete_input,
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        return f"Deleted course section {section_id} and all associated content links"
