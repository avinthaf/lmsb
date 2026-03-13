from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

@dataclass
class Category:
    id: UUID
    parent_id: Optional[UUID]
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None