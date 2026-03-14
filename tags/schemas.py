from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

@dataclass
class Tag:
    id: UUID
    name: str
    description: str
    school_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None