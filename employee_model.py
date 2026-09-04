from pydantic import BaseModel, EmailStr
from typing import Optional


class AddReq(BaseModel):
    email: EmailStr
    name: str
    age: int
    address: str
    aadhar_number: str
    status: str = "active"
    date_of_joining: Optional[str] = None   # format: "YYYY-MM-DD"


class ModifyReq(BaseModel):
    employee_id: int
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[str] = None
    aadhar_number: Optional[str] = None
    status: Optional[str] = None
    date_of_joining: Optional[str] = None


class DeleteReq(BaseModel):
    employee_id: int


class AddLeaveReq(BaseModel):
    employee_id: int
    financial_year: str          # e.g. "2025-2026"
    sick_leave: int = 12
    casual_leave: int = 12
    sick_leave_taken: int = 0
    casual_leave_taken: int = 0