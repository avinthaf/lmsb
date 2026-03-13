# PU 1 - Create Platform User

## API Layer
1. A user creates an account with the Authentication Service
2. The Authentication Service sends a webhook to /webhooks/platform_users
3. The webhook handler creates a platform user record in the database (use the same uuid for platform_user.id as the Authentication Service)


