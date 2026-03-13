from flask import Blueprint, request
from lib.auth import get_user_id_from_token
from courses.workflows import CreateCourseWorkflow
import uuid

courses_bp = Blueprint('courses', __name__)

ROLES_CACHE = {}
_temporal_client = None

def init_courses(roles_cache, temporal_client_getter):
    """Initialize courses blueprint with shared resources"""
    global ROLES_CACHE, _temporal_client
    ROLES_CACHE = roles_cache
    _temporal_client = temporal_client_getter
    
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