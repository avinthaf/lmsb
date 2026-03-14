from flask import Blueprint, request
from lib.auth import get_user_id_from_token
from lib.db import db_client

assessments_bp = Blueprint('assessments', __name__)

@assessments_bp.route("/assessments/<assessment_id>", methods=["PUT"])
async def update_assessment(assessment_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Get request body
    data = request.get_json()
    
    # Build update data with only provided fields
    update_data = {}
    
    if data.get('name') is not None:
        update_data["name"] = data.get('name')
    if data.get('description') is not None:
        update_data["description"] = data.get('description')
    
    # Only update if there's something to update
    if not update_data:
        return {"error": "No fields to update"}, 400
    
    response = (
        db_client.table("assessments")
        .update(update_data)
        .eq("id", assessment_id)
        .execute()
    )
    
    if not response.data:
        return {"error": "Assessment not found"}, 404
    
    return {"assessment": response.data[0]}, 200
