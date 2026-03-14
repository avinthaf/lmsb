from flask import Flask, request
from flask_cors import CORS
from platform_users import CreatePlatformUserInput
from workflows import CreatePlatformUserWorkflow
from lib.auth import get_user_id_from_token
from api import register_blueprints
from api.organizations import init_organizations
from api.schools import init_schools
from api.categories import init_categories
from api.courses import init_courses
from temporalio.client import Client
import os
import asyncio
from typing import Dict, List

app = Flask(__name__)

# Apply CORS before registering blueprints
CORS(app, 
     origins=["http://localhost:5173", "http://127.0.0.1:5173"],
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     expose_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

# Initialize Temporal client (will be set on first use)
_temporal_client = None

# Global cache for roles
ROLES_CACHE: Dict[str, str] = {}

def load_roles():
    """Load roles from database at startup and cache them"""
    from lib import db_client
    response = db_client.table("roles").select("id, name").execute()
    global ROLES_CACHE
    # Create a dict mapping role name to role id for easy lookup
    ROLES_CACHE = {role['name']: role['id'] for role in response.data}
    print(f"Loaded {len(ROLES_CACHE)} roles into API cache: {list(ROLES_CACHE.keys())}")

async def get_temporal_client():
    global _temporal_client
    if _temporal_client is None:
        temporal_url = os.environ.get("TEMPORAL_URL", "localhost:7233")
        _temporal_client = await Client.connect(temporal_url)
    return _temporal_client

# Load roles when the module is imported
load_roles()

# Initialize blueprints with shared resources
init_organizations(ROLES_CACHE, get_temporal_client)
init_schools(ROLES_CACHE, get_temporal_client)
init_categories(get_temporal_client)
init_courses(ROLES_CACHE, get_temporal_client)

# Register all API blueprints
register_blueprints(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/webhooks/platform_users/create", methods=["POST"])
async def platform_users_webhook():
    data = request.get_json()
    # Create platform user in database using Temporal workflow
    platform_user_input = CreatePlatformUserInput(
        id=data['record']['id'], 
        email=data['record']['email']
    )
    
    # Start Temporal workflow
    client = await get_temporal_client()
    workflow_id = f"create-platform-user-{data['record']['id']}"
    
    await client.start_workflow(
        CreatePlatformUserWorkflow.run,
        platform_user_input,
        id=workflow_id,
        task_queue="main"
    )
    
    print(f"Received webhook data: {data}")
    return {"status": "received", "workflow_id": workflow_id}, 200
