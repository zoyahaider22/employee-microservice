from pydantic import BaseModel, EmailStr
from typing import Optional


class AddReq(BaseModel):
    email: EmailStr
    name: str
    age: int
    address: str
    aadhar_number: str
    status: str = "active"


class ModifyReq(BaseModel):
    employee_id: int
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[str] = None
    aadhar_number: Optional[str] = None
    status: Optional[str] = None


class DeleteReq(BaseModel):
    employee_id: int