from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from courses.schemas import CreateCourseContentInput

@workflow.defn(name="CreateCourseContentWorkflow")
class CreateCourseContentWorkflow:
    @workflow.run
    async def run(self, school_id: str, course_content_type_id: str, name: str, section_id: str, order: int = None) -> str:
        # Step 1: Create the course content
        content_input = CreateCourseContentInput(
            school_id=school_id,
            course_content_type_id=course_content_type_id,
            name=name,
            section_id=section_id,
            order=order
        )
        content_result = await workflow.execute_activity(
            "create_course_content",
            content_input,
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        # Step 2: Link course content to section
        await workflow.execute_activity(
            "link_course_content_to_section",
            {"section_id": section_id, "content_id": content_result},
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        return f"Created course content {content_result} and linked to section {section_id}"
