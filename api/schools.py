from flask import Blueprint, request
from lib.auth import get_user_id_from_token
from lib.db import db_client
from schools.schemas import CreateSchoolInput
import uuid

schools_bp = Blueprint('schools', __name__)

ROLES_CACHE = {}
_temporal_client = None

def init_schools(roles_cache, temporal_client_getter):
    """Initialize schools blueprint with shared resources"""
    global ROLES_CACHE, _temporal_client
    ROLES_CACHE = roles_cache
    _temporal_client = temporal_client_getter
    
@schools_bp.route("/schools", methods=["POST"])
async def create_school():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Get request body
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'organization_id', 'school_industry_id', 'subdomain']
    for field in required_fields:
        if not data.get(field):
            return {"error": f"{field} is required"}, 400
    
    # Create school
    response = (
        db_client.table("schools")
        .insert({
            "name": data.get('name'),
            "logo_url": data.get('logo_url'),
            "organization_id": data.get('organization_id'),
            "school_industry_id": data.get('school_industry_id'),
            "subdomain": data.get('subdomain')
        })
        .execute()
    )

    return {"school": response.data[0]}, 200

@schools_bp.route("/schools", methods=["GET"])
async def get_schools():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Get organization_id from query params
    org_id = request.args.get('organization_id')
    
    if not org_id:
        return {"error": "Organization ID is required"}, 400
    
    # Fetch schools where user is a member through their organization
    response = (
        db_client.table("schools")
        .select("*")
        .eq("organization_id", org_id)
        .execute()
    )
    
    # Extract schools from all organizations the user belongs to
    schools = []
    for school in response.data:
        schools.append(school)
    
    return {"schools": schools}, 200

@schools_bp.route("/school_industries", methods=["GET"])
async def get_school_industries():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Fetch all school industries
    response = (
        db_client.table("school_industries")
        .select("*")
        .execute()
    )
    
    return {"school_industries": response.data}, 200