from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

@dataclass
class PlatformUser:
    id: UUID
    auth_id: UUID
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@dataclass
class CreatePlatformUserInput:
    id: UUID
    email: str

@dataclass
class GetPlatformUserInput:
    email: str
