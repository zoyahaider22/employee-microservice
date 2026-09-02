from fastapi import HTTPException
from employee_model import AddReq, ModifyReq, DeleteReq
import employee_repository as repo
import rabbitmq_publisher


def add_employee_controller(e: AddReq):
    if repo.email_exists(e.email):
        raise HTTPException(400, "Email already exists")
    if repo.aadhar_exists(e.aadhar_number):
        raise HTTPException(400, "Aadhar number already exists")

    new_id = repo.add_employee(e.email, e.name, e.age, e.address, e.aadhar_number, e.status)

    rabbitmq_publisher.publish_employee_id(new_id)  # tell RabbitMQ about the new employee

    return {"message": "Employee added", "employee_id": new_id}


def modify_employee_controller(e: ModifyReq):
    success = repo.update_employee(
        e.employee_id, e.email, e.name, e.age, e.address, e.aadhar_number, e.status
    )
    if not success:
        raise HTTPException(404, "Employee not found")
    return {"message": "Employee updated"}


def delete_employee_controller(e: DeleteReq):
    success = repo.delete_employee(e.employee_id)
    if not success:
        raise HTTPException(404, "Employee not found")
    return {"message": "Employee deleted"}


def get_employee_controller(employee_id: int):
    employee = repo.get_employee(employee_id)
    if not employee:
        raise HTTPException(404, "Employee not found")
    return employee


def get_all_employees_controller():
    return repo.get_all_employees()