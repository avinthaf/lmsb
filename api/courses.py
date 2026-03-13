from flask import Blueprint, request
from lib.auth import get_user_id_from_token
from lib.db import db_client
from courses.schemas import CreateCourseInput
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
    
    # Create course
    response = (
        db_client.table("courses")
        .insert({
            "school_id": data.get('school_id'),
            "name": data.get('name'),
            "description": data.get('description'),
            "category_id": data.get('category_id'),
            "credits": data.get('credits'),
            "cover_photo_url": data.get('cover_photo_url'),
            "url": data.get('url')
        })
        .execute()
    )

    return {"course": response.data[0]}, 200