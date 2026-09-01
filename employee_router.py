from fastapi import APIRouter
from employee_model import AddReq, ModifyReq, DeleteReq
import employee_controller as controller

router = APIRouter()


@router.post("/add")
def add(e: AddReq):
    return controller.add_employee_controller(e)


@router.post("/modify")
def modify(e: ModifyReq):
    return controller.modify_employee_controller(e)


@router.post("/delete")
def delete(e: DeleteReq):
    return controller.delete_employee_controller(e)


@router.get("/employees")
def list_all():
    return controller.get_all_employees_controller()


@router.get("/employees/{employee_id}")
def get_one(employee_id: int):
    return controller.get_employee_controller(employee_id)