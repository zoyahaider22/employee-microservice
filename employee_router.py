from fastapi import APIRouter
from employee_model import AddReq, ModifyReq, DeleteReq
import employee_controller as controller
from employee_model import AddLeaveReq
from employee_controller import add_leave_controller, get_employee_leaves_controller

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


@router.post("/leaves")
def add_leave(l: AddLeaveReq):
    return add_leave_controller(l)


@router.get("/employee/{employee_id}/leaves")
def get_employee_leaves(employee_id: int):
    return get_employee_leaves_controller(employee_id)