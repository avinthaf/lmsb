from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

@dataclass
class CreateSchoolInput:
    name: str
    organization_id: UUID
    school_industry_id: UUID
    subdomain: str
    logo_url: Optional[str] = None

    
@dataclass
class School:
    id: UUID
    name: str
    subdomain: str
    organization_id: UUID
    school_industry_id: UUID
    created_at: datetime
    updated_at: datetime
    logo_url: Optional[str] = None
    deleted_at: Optional[datetime] = None
    
@dataclass
class SchoolIndustry:
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    