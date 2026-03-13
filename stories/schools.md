# SC 1 - Create School

## API Layer
1. Client sends POST /schools with a JWT
2. Authentication middleware validates the JWT and extracts the user_id
3. Request body is validated
4. Fetch the org_id from the Organization Service using user_id
   - if no org found, return 400/403 immediately
5. CreateSchoolWorkflow is started in Temporal with { user_id, org_id, school_name, ... }

## Saga (Temporal Workflow)
6. Create a school record in the Schools Service { org_id, school_name, ... }
   - compensate: delete the school
   