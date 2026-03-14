from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from courses.schemas import CreateCourseContentInput
    from assessments.schemas import CreateAssessmentInput

@workflow.defn(name="CreateCourseContentWorkflow")
class CreateCourseContentWorkflow:
    @workflow.run
    async def run(self, school_id: str, course_content_type_id: str, name: str, section_id: str, content_type_label: str, order: int = None) -> str:
        assessment_id = None
        
        workflow.logger.info(f"[WORKFLOW] CreateCourseContentWorkflow - content_type_label: '{content_type_label}'")
        
        # Step 1: If this is an Assessment, create the assessment first
        if content_type_label == "Assessment":
            workflow.logger.info(f"[WORKFLOW] Creating assessment for Assessment type")
            assessment_input = CreateAssessmentInput(
                school_id=school_id,
                name=name
            )
            assessment_id = await workflow.execute_activity(
                "create_assessment",
                assessment_input,
                start_to_close_timeout=timedelta(seconds=10),
            )
        
        # Step 2: Create the course content
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
        
        # Step 3: If we created an assessment, update the course content's ref_id
        if assessment_id:
            await workflow.execute_activity(
                "update_course_content_ref_id",
                {"content_id": content_result, "ref_id": assessment_id},
                start_to_close_timeout=timedelta(seconds=10),
            )
        
        # Step 4: Link course content to section
        await workflow.execute_activity(
            "link_course_content_to_section",
            {"section_id": section_id, "content_id": content_result},
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        result_msg = f"Created course content {content_result} and linked to section {section_id}"
        if assessment_id:
            result_msg += f" with assessment {assessment_id}"
        return result_msg
