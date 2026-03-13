from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from .schemas import CreateCourseInput, CreateCourseAuthorInput, CreateCourseSectionInput, CreateCourseContentInput, DeleteCourseContentInput

@workflow.defn(name="CreateCourseWorkflow")
class CreateCourseWorkflow:
    @workflow.run
    async def run(self, user_id: str, school_id: str, name: str, category_id: str, credits: int, url: str, description: str = None, cover_photo_url: str = None) -> str:
        # Step 1: Create the course
        course_input = CreateCourseInput(
            school_id=school_id,
            name=name,
            category_id=category_id,
            credits=credits,
            url=url,
            description=description,
            cover_photo_url=cover_photo_url
        )
        course_result = await workflow.execute_activity(
            "create_course",
            course_input,
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        # Step 2: Create the course author with the returned course_id
        author_input = CreateCourseAuthorInput(
            course_id=course_result,
            user_id=user_id
        )
        author_result = await workflow.execute_activity(
            "create_course_author",
            author_input,
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        # Step 3: Create an untitled course section
        section_input = CreateCourseSectionInput(
            course_id=course_result,
            name=None,  # Untitled section
            order=None  # Will be auto-assigned by database
        )
        section_result = await workflow.execute_activity(
            "create_course_section",
            section_input,
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        return f"Created course {course_result} with author {user_id} and section {section_result}"

@workflow.defn(name="CreateCourseContentWorkflow")
class CreateCourseContentWorkflow:
    @workflow.run
    async def run(self, school_id: str, course_content_type_id: str, name: str, order: int, section_id: str) -> str:
        # Step 1: Create the course content
        content_input = CreateCourseContentInput(
            school_id=school_id,
            course_content_type_id=course_content_type_id,
            name=name,
            order=order,
            section_id=section_id
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
