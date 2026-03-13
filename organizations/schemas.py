from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

@dataclass
class CreateOrganizationInput:
    name: str
    
@dataclass
class CreateOrganizationMemberInput:
    organization_id: str
    user_id: str
    role_id: str
    
@dataclass
class Organization:
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
@dataclass
class OrganizationMember:
    id: UUID
    organization_id: UUID
    user_id: UUID
    role_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None