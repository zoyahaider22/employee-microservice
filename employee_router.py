from fastapi import APIRouter, HTTPException
from employee_model import AddReq, ModifyReq, DeleteReq
import employee_repository as repo

router = APIRouter()


@router.post("/add")
def add(e: AddReq):
    if repo.email_exists(e.email):
        raise HTTPException(400, "Email already exists")
    if repo.aadhar_exists(e.aadhar_number):
        raise HTTPException(400, "Aadhar number already exists")

    new_id = repo.add_employee(e.email, e.name, e.age, e.address, e.aadhar_number, e.status)
    return {"message": "Employee added", "employee_id": new_id}


@router.post("/modify")
def modify(e: ModifyReq):
    success = repo.update_employee(
        e.employee_id, e.email, e.name, e.age, e.address, e.aadhar_number, e.status
    )
    if not success:
        raise HTTPException(404, "Employee not found")
    return {"message": "Employee updated"}


@router.post("/delete")
def delete(e: DeleteReq):
    success = repo.delete_employee(e.employee_id)
    if not success:
        raise HTTPException(404, "Employee not found")
    return {"message": "Employee deleted"}


@router.get("/employees")
def list_all():
    return repo.get_all_employees()


@router.get("/employees/{employee_id}")
def get_one(employee_id: int):
    employee = repo.get_employee(employee_id)
    if not employee:
        raise HTTPException(404, "Employee not found")
    return employee