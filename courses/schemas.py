from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

@dataclass
class CreateCourseInput:
    school_id: str
    name: str
    category_id: str
    credits: int
    url: str
    description: Optional[str]
    cover_photo_url: Optional[str]

@dataclass
class Course:
    id: UUID
    school_id: UUID
    name: str
    category_id: UUID
    course_status_id: UUID
    credits: int
    url: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    description: Optional[str]
    cover_photo_url: Optional[str]