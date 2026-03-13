from flask import Blueprint, request
from lib.auth import get_user_id_from_token
from lib.db import db_client
from workflows import CreateOrganizationWorkflow
import uuid

organizations_bp = Blueprint('organizations', __name__)

ROLES_CACHE = {}
_temporal_client = None

def init_organizations(roles_cache, temporal_client_getter):
    """Initialize organizations blueprint with shared resources"""
    global ROLES_CACHE, _temporal_client
    ROLES_CACHE = roles_cache
    _temporal_client = temporal_client_getter

@organizations_bp.route("/organizations", methods=["POST"])
async def create_organization():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Get request body
    data = request.get_json()
    org_name = data.get('name')
    
    if not org_name:
        return {"error": "Organization name is required"}, 400
    
    # Get organization:owner role ID from cache
    owner_role_id = ROLES_CACHE.get('organization:owner')
    if not owner_role_id:
        return {"error": "Owner role not found"}, 500
    
    # Start CreateOrganizationWorkflow
    client = await _temporal_client()
    workflow_id = f"create-org-{uuid.uuid4()}"
    
    await client.start_workflow(
        CreateOrganizationWorkflow.run,
        args=[user_id, org_name, owner_role_id],
        id=workflow_id,
        task_queue="main"
    )
    
    return {"status": "workflow_started", "workflow_id": workflow_id}, 200

@organizations_bp.route("/organizations", methods=["GET"])
async def get_organizations():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Fetch organizations where user is a member
    response = (
        db_client.table("organization_members")
        .select("organization_id, organizations(id, name, created_at)")
        .eq("user_id", user_id)
        .execute()
    )
    
    # Extract organization data from the join
    organizations = [member['organizations'] for member in response.data if member.get('organizations')]
    
    return {"organizations": organizations}, 200
