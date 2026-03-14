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
    
@dataclass
class CreateCourseAuthorInput:
    course_id: UUID
    user_id: UUID

@dataclass
class CourseAuthor:
    id: UUID
    course_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@dataclass
class CourseStatus:
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

@dataclass
class CourseGroup:
    id: UUID
    school_id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@dataclass
class CourseGroupUser:
    id: UUID
    course_group_id: UUID
    user_id: UUID
    role_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@dataclass
class CoursesCourseGroup:
    id: UUID
    course_id: UUID
    course_group_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@dataclass
class CreateCourseSectionInput:
    course_id: UUID
    name: Optional[str] = None
    order: Optional[int] = None

@dataclass
class UpdateCourseSectionInput:
    section_id: UUID
    name: Optional[str] = None
    order: Optional[int] = None

@dataclass
class CreateCourseContentInput:
    school_id: str
    course_content_type_id: str
    name: str
    order: int
    section_id: str

@dataclass
class DeleteCourseContentInput:
    content_id: str

@dataclass
class CourseSection:
    id: UUID
    course_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    name: Optional[str] = None
    order: Optional[int] = None

@dataclass
class CourseContentTypeType:
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

@dataclass
class CourseContentTypeSubtype:
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

@dataclass
class CourseContentType:
    id: UUID
    label: str
    type_id: UUID
    subtype_id: UUID
    description: str
    created_at: datetime
    updated_at: datetime

@dataclass
class CourseContent:
    id: UUID
    school_id: UUID
    course_content_type_id: UUID
    name: str
    order: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@dataclass
class CourseSectionsCourseContent:
    id: UUID
    course_section_id: UUID
    course_content_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@dataclass
class CourseContentItem:
    id: UUID
    school_id: UUID
    order: int
    ref_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@dataclass
class CourseContentsCourseContentItem:
    id: UUID
    course_content_id: UUID
    course_content_item_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None