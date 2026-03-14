from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

@dataclass
class MediaVideo:
    id: UUID
    url: str
    thumbnail_id: UUID
    duration: int
    school_id: UUID
    category_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@dataclass
class MediaImage:
    id: UUID
    url: str
    school_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@dataclass
class MediaTag:
    id: UUID
    tag_id: UUID
    media_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None