from flask import Blueprint, request
from lib.auth import get_user_id_from_token
from lib.db import db_client
import uuid

categories_bp = Blueprint('categories', __name__)

_temporal_client = None

def init_categories(temporal_client_getter):
    """Initialize categories blueprint with shared resources"""
    global _temporal_client
    _temporal_client = temporal_client_getter
    
@categories_bp.route("/categories", methods=["GET"])
async def get_categories():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    # Get all categories
    response = (
        db_client.table("categories")
        .select('*')
        .execute()
    )

    return {"categories": response.data}, 200