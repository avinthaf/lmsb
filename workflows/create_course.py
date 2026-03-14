from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from courses.schemas import CreateCourseInput, CreateCourseAuthorInput, CreateCourseSectionInput

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
