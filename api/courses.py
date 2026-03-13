from flask import Blueprint, request
from lib.auth import get_user_id_from_token
from lib.db import db_client
from courses.workflows import CreateCourseWorkflow
from datetime import datetime
import uuid

courses_bp = Blueprint('courses', __name__)

ROLES_CACHE = {}
_temporal_client = None

def init_courses(roles_cache, temporal_client_getter):
    """Initialize courses blueprint with shared resources"""
    global ROLES_CACHE, _temporal_client
    ROLES_CACHE = roles_cache
    _temporal_client = temporal_client_getter

def is_course_author(user_id: str, course_id: str) -> bool:
    """Check if user is an author of the course"""
    response = (
        db_client.table("course_authors")
        .select("id")
        .eq("user_id", user_id)
        .eq("course_id", course_id)
        .is_("deleted_at", "null")
        .execute()
    )
    return len(response.data) > 0
    
@courses_bp.route("/courses", methods=["POST"])
async def create_course():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Get request body
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['school_id', 'name', 'category_id', 'credits', 'url']
    for field in required_fields:
        if not data.get(field):
            return {"error": f"{field} is required"}, 400
    
    # Start CreateCourseWorkflow
    client = await _temporal_client()
    workflow_id = f"create-course-{uuid.uuid4()}"
    
    await client.start_workflow(
        CreateCourseWorkflow.run,
        args=[
            user_id,
            data.get('school_id'),
            data.get('name'),
            data.get('category_id'),
            data.get('credits'),
            data.get('url'),
            data.get('description'),
            data.get('cover_photo_url')
        ],
        id=workflow_id,
        task_queue="main"
    )
    
    return {"status": "workflow_started", "workflow_id": workflow_id}, 200

@courses_bp.route("/courses/<course_id>", methods=["GET"])
async def get_course(course_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Fetch course by ID
    response = (
        db_client.table("courses")
        .select("*")
        .eq("id", course_id)
        .is_("deleted_at", "null")
        .execute()
    )
    
    if not response.data:
        return {"error": "Course not found"}, 404
    
    return {"course": response.data[0]}, 200

@courses_bp.route("/courses/<course_id>/sections", methods=["POST"])
async def create_course_section(course_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Check if user is a course author
    if not is_course_author(user_id, course_id):
        return {"error": "Unauthorized: You must be a course author"}, 403
    
    # Get request body
    data = request.get_json()
    
    # Build insert data with required fields
    insert_data = {
        "course_id": course_id,
    }
    
    # Only add optional fields if they are not None
    if data.get('name') is not None:
        insert_data["name"] = data.get('name')
    if data.get('order') is not None:
        insert_data["order"] = data.get('order')
    
    response = db_client.table("course_sections").insert(insert_data).execute()
    
    return {"section": response.data[0]}, 200

@courses_bp.route("/courses/<course_id>/sections/<section_id>", methods=["PUT"])
async def update_course_section(course_id, section_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Check if user is a course author
    if not is_course_author(user_id, course_id):
        return {"error": "Unauthorized: You must be a course author"}, 403
    
    # Get request body
    data = request.get_json()
    
    # Build update data with only provided fields
    update_data = {}
    
    if data.get('name') is not None:
        update_data["name"] = data.get('name')
    if data.get('order') is not None:
        update_data["order"] = data.get('order')
    
    # Only update if there's something to update
    if not update_data:
        return {"error": "No fields to update"}, 400
    
    response = (
        db_client.table("course_sections")
        .update(update_data)
        .eq("id", section_id)
        .eq("course_id", course_id)
        .execute()
    )
    
    if not response.data:
        return {"error": "Section not found"}, 404
    
    return {"section": response.data[0]}, 200

@courses_bp.route("/courses/<course_id>/sections/<section_id>", methods=["DELETE"])
async def delete_course_section(course_id, section_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Check if user is a course author
    if not is_course_author(user_id, course_id):
        return {"error": "Unauthorized: You must be a course author"}, 403
    
    # Soft delete by setting deleted_at timestamp
    response = (
        db_client.table("course_sections")
        .update({"deleted_at": datetime.utcnow().isoformat()})
        .eq("id", section_id)
        .eq("course_id", course_id)
        .execute()
    )
    
    if not response.data:
        return {"error": "Section not found"}, 404
    
    return {"message": "Section deleted successfully", "section_id": section_id}, 200

@courses_bp.route("/courses/<course_id>/sections", methods=["GET"])
async def get_course_sections(course_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Fetch sections for the course, excluding soft-deleted ones
    response = (
        db_client.table("course_sections")
        .select("*")
        .eq("course_id", course_id)
        .is_("deleted_at", "null")
        .order("order")
        .execute()
    )
    
    return {"sections": response.data}, 200

@courses_bp.route("/courses/<course_id>/sections/<section_id>/contents", methods=["POST"])
async def create_course_content(course_id, section_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Check if user is a course author
    if not is_course_author(user_id, course_id):
        return {"error": "Unauthorized: You must be a course author"}, 403
    
    # Get request body
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['school_id', 'course_content_type_id', 'name', 'order']
    for field in required_fields:
        if not data.get(field):
            return {"error": f"{field} is required"}, 400
    
    # Start CreateCourseContentWorkflow
    client = await _temporal_client()
    workflow_id = f"create-course-content-{uuid.uuid4()}"
    
    await client.start_workflow(
        "CreateCourseContentWorkflow",
        args=[
            data.get('school_id'),
            data.get('course_content_type_id'),
            data.get('name'),
            data.get('order'),
            section_id
        ],
        id=workflow_id,
        task_queue="main"
    )
    
    return {"status": "workflow_started", "workflow_id": workflow_id}, 200

@courses_bp.route("/courses/<course_id>/sections/<section_id>/contents/<content_id>", methods=["PUT"])
async def update_course_content(course_id, section_id, content_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Check if user is a course author
    if not is_course_author(user_id, course_id):
        return {"error": "Unauthorized: You must be a course author"}, 403
    
    # Get request body
    data = request.get_json()
    
    # Build update data with only provided fields
    update_data = {}
    
    if data.get('name') is not None:
        update_data["name"] = data.get('name')
    if data.get('order') is not None:
        update_data["order"] = data.get('order')
    
    # Only update if there's something to update
    if not update_data:
        return {"error": "No fields to update"}, 400
    
    response = (
        db_client.table("course_contents")
        .update(update_data)
        .eq("id", content_id)
        .execute()
    )
    
    if not response.data:
        return {"error": "Content not found"}, 404
    
    return {"content": response.data[0]}, 200

@courses_bp.route("/courses/<course_id>/sections/<section_id>/contents/<content_id>", methods=["DELETE"])
async def delete_course_content(course_id, section_id, content_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Check if user is a course author
    if not is_course_author(user_id, course_id):
        return {"error": "Unauthorized: You must be a course author"}, 403
    
    # Start DeleteCourseContentWorkflow
    client = await _temporal_client()
    workflow_id = f"delete-course-content-{uuid.uuid4()}"
    
    await client.start_workflow(
        "DeleteCourseContentWorkflow",
        args=[content_id],
        id=workflow_id,
        task_queue="main"
    )
    
    return {"status": "workflow_started", "workflow_id": workflow_id, "message": "Content and associated links are being deleted"}, 200

@courses_bp.route("/course-content-types", methods=["GET"])
async def get_course_content_types():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Fetch all course content types
    response = (
        db_client.table("course_content_types")
        .select("*")
        .order("name")
        .execute()
    )
    
    return {"course_content_types": response.data}, 200

