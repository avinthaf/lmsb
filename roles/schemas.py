from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

@dataclass
class Role:
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
@dataclass
class Scope:
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
@dataclass
class RoleScope:
    id: UUID
    role_id: UUID
    scope_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    