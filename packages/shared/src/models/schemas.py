from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

class Organization(BaseModel):
    id: UUID
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime

class Role(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: datetime

class User(BaseModel):
    id: UUID
    organization_id: UUID
    clerk_id: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

class Employee(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    department: Optional[str] = None
    role_title: Optional[str] = None
    system_prompt: str
    working_hours: Dict[str, Any] = Field(
        default_factory=lambda: {"start": "09:00", "end": "17:00", "days": [1, 2, 3, 4, 5]}
    )
    timezone: str = "UTC"
    escalation_rules: Dict[str, Any] = Field(default_factory=lambda: {"on_error": "notify_slack"})
    approval_rules: Dict[str, Any] = Field(default_factory=lambda: {"require_approval_for": []})
    created_at: datetime
    updated_at: datetime

class Conversation(BaseModel):
    id: UUID
    organization_id: UUID
    employee_id: UUID
    title: Optional[str] = None
    status: str = "active"
    created_at: datetime
    updated_at: datetime

class Task(BaseModel):
    id: UUID
    organization_id: UUID
    employee_id: UUID
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class ToolCall(BaseModel):
    id: UUID
    workflow_run_id: Optional[UUID] = None
    employee_id: UUID
    tool_name: str
    arguments: Dict[str, Any]
    response: Optional[str] = None
    status: str
    error_message: Optional[str] = None
    duration_ms: Optional[int] = None
    created_at: datetime

class AuditLog(BaseModel):
    id: UUID
    organization_id: UUID
    user_id: Optional[UUID] = None
    action: str
    target_id: Optional[UUID] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
