# ORG 1 - Create Organization

## API Layer
1. Client sends POST /organizations with a JWT
2. Authentication middleware validates the JWT and extracts the user_id
3. Request body is validated
4. CreateOrganizationWorkflow is started in Temporal with { user_id, org_name, ... }

## Worker Startup
- Fetch and cache role IDs from the Roles Service (admin, member, etc.)

## Saga (Temporal Workflow)
5. Create an organization record in the Organization Service
   - compensate: delete the organization
6. Create an organization member record in the Organization Service
   { org_id, user_id, role_id: CACHED_ADMIN_ROLE_ID }
   - compensate: delete the organization member