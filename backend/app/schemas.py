from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class EmployeeBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=200)
    job_title: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    salary: float = Field(..., gt=0)
    department: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=1, max_length=200)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=200)
    job_title: str | None = Field(None, min_length=1, max_length=100)
    country: str | None = Field(None, min_length=1, max_length=100)
    salary: float | None = Field(None, gt=0)
    department: str | None = Field(None, min_length=1, max_length=100)
    email: str | None = Field(None, min_length=1, max_length=200)


class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
