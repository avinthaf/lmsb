from dataclasses import dataclass
from temporalio import activity
from lib.db import db_client
from .schemas import CreateCourseInput, CreateCourseAuthorInput

@activity.defn(name="create_course")
async def create(input: CreateCourseInput) -> str:
    print(f"[ACTIVITY] create_course started with input: {input}")
    try:
        response = (
            db_client.table("courses")
            .insert({
                "school_id": input.school_id,
                "name": input.name,
                "category_id": input.category_id,
                "credits": input.credits,
                "url": input.url,
                "description": input.description,
                "cover_photo_url": input.cover_photo_url
            })
            .execute()
        )
        print(f"[ACTIVITY] create_course DB response: {response.data}")
        # Return the course ID from the created record
        course_id = response.data[0]['id']
        print(f"[ACTIVITY] create_course completed, course_id: {course_id}")
        return course_id
    except Exception as e:
        print(f"[ACTIVITY] create_course ERROR: {type(e).__name__}: {e}")
        raise

@activity.defn(name="create_course_author")
async def create_author(input: CreateCourseAuthorInput) -> str:
    print(f"[ACTIVITY] create_course_author started with input: {input}")
    try:
        response = (
            db_client.table("course_authors")
            .insert({
                "course_id": str(input.course_id),
                "user_id": str(input.user_id)
            })
            .execute()
        )
        print(f"[ACTIVITY] create_course_author DB response: {response.data}")
        # Return the course author ID from the created record
        author_id = response.data[0]['id']
        print(f"[ACTIVITY] create_course_author completed, author_id: {author_id}")
        return author_id
    except Exception as e:
        print(f"[ACTIVITY] create_course_author ERROR: {type(e).__name__}: {e}")
        raise
