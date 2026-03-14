from dataclasses import dataclass
from temporalio import activity
from lib.db import db_client
from datetime import datetime
from typing import Dict
from .schemas import CreateCourseInput, CreateCourseAuthorInput, CreateCourseSectionInput, CreateCourseContentInput, DeleteCourseContentInput

@activity.defn(name="create_course")
async def create(input: CreateCourseInput) -> str:
    print(f"[ACTIVITY] create_course started with input: {input}")
    try:
        # Build insert data, filtering out None values to allow database defaults
        insert_data = {
            "school_id": input.school_id,
            "name": input.name,
            "category_id": input.category_id,
            "credits": input.credits,
            "url": input.url,
        }
        
        # Only add optional fields if they are not None
        if input.description is not None:
            insert_data["description"] = input.description
        if input.cover_photo_url is not None:
            insert_data["cover_photo_url"] = input.cover_photo_url
        
        response = db_client.table("courses").insert(insert_data).execute()
        
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

@activity.defn(name="create_course_section")
async def create_section(input: CreateCourseSectionInput) -> str:
    print(f"[ACTIVITY] create_course_section started with input: {input}")
    try:
        # Build insert data with required fields
        insert_data = {
            "course_id": str(input.course_id),
        }
        
        # Only add optional fields if they are not None
        if input.name is not None:
            insert_data["name"] = input.name
        if input.order is not None:
            insert_data["order"] = input.order
        
        response = db_client.table("course_sections").insert(insert_data).execute()
        
        print(f"[ACTIVITY] create_course_section DB response: {response.data}")
        # Return the section ID from the created record
        section_id = response.data[0]['id']
        print(f"[ACTIVITY] create_course_section completed, section_id: {section_id}")
        return section_id
    except Exception as e:
        print(f"[ACTIVITY] create_course_section ERROR: {type(e).__name__}: {e}")
        raise

@activity.defn(name="create_course_content")
async def create_content(input: CreateCourseContentInput) -> str:
    print(f"[ACTIVITY] create_course_content started with input: {input}")
    try:
        insert_data = {
            "school_id": input.school_id,
            "course_content_type_id": input.course_content_type_id,
            "name": input.name
        }
        
        # Only include order if it's provided
        if input.order is not None:
            insert_data["order"] = input.order
        
        response = db_client.table("course_contents").insert(insert_data).execute()
        
        print(f"[ACTIVITY] create_course_content DB response: {response.data}")
        content_id = response.data[0]['id']
        print(f"[ACTIVITY] create_course_content completed, content_id: {content_id}")
        return content_id
    except Exception as e:
        print(f"[ACTIVITY] create_course_content ERROR: {type(e).__name__}: {e}")
        raise

@activity.defn(name="link_course_content_to_section")
async def link_content_to_section(input: dict) -> str:
    print(f"[ACTIVITY] link_course_content_to_section started with input: {input}")
    try:
        insert_data = {
            "course_section_id": input["section_id"],
            "course_content_id": input["content_id"]
        }
        
        response = db_client.table("course_sections_course_contents").insert(insert_data).execute()
        
        print(f"[ACTIVITY] link_course_content_to_section DB response: {response.data}")
        link_id = response.data[0]['id']
        print(f"[ACTIVITY] link_course_content_to_section completed, link_id: {link_id}")
        return link_id
    except Exception as e:
        print(f"[ACTIVITY] link_course_content_to_section ERROR: {type(e).__name__}: {e}")
        raise

@activity.defn(name="delete_course_content")
async def delete_content(input: DeleteCourseContentInput) -> str:
    print(f"[ACTIVITY] delete_course_content started with input: {input}")
    try:
        response = (
            db_client.table("course_contents")
            .update({"deleted_at": datetime.utcnow().isoformat()})
            .eq("id", input.content_id)
            .execute()
        )
        
        print(f"[ACTIVITY] delete_course_content DB response: {response.data}")
        print(f"[ACTIVITY] delete_course_content completed, content_id: {input.content_id}")
        return input.content_id
    except Exception as e:
        print(f"[ACTIVITY] delete_course_content ERROR: {type(e).__name__}: {e}")
        raise

@activity.defn(name="delete_course_content_links")
async def delete_content_links(input: DeleteCourseContentInput) -> str:
    print(f"[ACTIVITY] delete_course_content_links started with input: {input}")
    try:
        response = (
            db_client.table("course_sections_course_contents")
            .update({"deleted_at": datetime.utcnow().isoformat()})
            .eq("course_content_id", input.content_id)
            .execute()
        )
        
        print(f"[ACTIVITY] delete_course_content_links DB response: {response.data}")
        affected_count = len(response.data) if response.data else 0
        print(f"[ACTIVITY] delete_course_content_links completed, affected {affected_count} links")
        return f"Deleted {affected_count} links"
    except Exception as e:
        print(f"[ACTIVITY] delete_course_content_links ERROR: {type(e).__name__}: {e}")
        raise

@activity.defn(name="update_course_content_ref_id")
async def update_content_ref_id(input: dict) -> str:
    print(f"[ACTIVITY] update_course_content_ref_id started with input: {input}")
    try:
        response = (
            db_client.table("course_contents")
            .update({"ref_id": input["ref_id"]})
            .eq("id", input["content_id"])
            .execute()
        )
        
        print(f"[ACTIVITY] update_course_content_ref_id DB response: {response.data}")
        print(f"[ACTIVITY] update_course_content_ref_id completed")
        return f"Updated course content {input['content_id']} with ref_id {input['ref_id']}"
    except Exception as e:
        print(f"[ACTIVITY] update_course_content_ref_id ERROR: {type(e).__name__}: {e}")
        raise
