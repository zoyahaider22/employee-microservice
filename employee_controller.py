from fastapi import HTTPException
import logging

from employee_model import AddReq, ModifyReq, DeleteReq
import employee_repository as repo
import rabbitmq_publisher


logger = logging.getLogger(__name__)


def add_employee_controller(e: AddReq):
    try:
        if repo.email_exists(e.email):
            logger.warning("Attempt to add employee with existing email: %s", e.email)
            raise HTTPException(400, "Email already exists")

        if repo.aadhar_exists(e.aadhar_number):
            logger.warning(
                "Attempt to add employee with existing Aadhar number"
            )
            raise HTTPException(400, "Aadhar number already exists")

        new_id = repo.add_employee(
            e.email,
            e.name,
            e.age,
            e.address,
            e.aadhar_number,
            e.status
        )

        logger.info("Employee %s added successfully", new_id)

        rabbitmq_publisher.publish_employee_id(new_id)

        logger.info(
            "Employee %s event published to RabbitMQ",
            new_id
        )

        return {
            "message": "Employee added",
            "employee_id": new_id
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error while adding employee")
        raise HTTPException(
            status_code=500,
            detail="Failed to add employee"
        )


def modify_employee_controller(e: ModifyReq):
    try:
        success = repo.update_employee(
            e.employee_id,
            e.email,
            e.name,
            e.age,
            e.address,
            e.aadhar_number,
            e.status
        )

        if not success:
            logger.warning(
                "Employee %s not found for update",
                e.employee_id
            )
            raise HTTPException(404, "Employee not found")

        logger.info(
            "Employee %s updated successfully",
            e.employee_id
        )

        return {"message": "Employee updated"}

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Unexpected error while updating employee %s",
            e.employee_id
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to update employee"
        )


def delete_employee_controller(e: DeleteReq):
    try:
        success = repo.delete_employee(e.employee_id)

        if not success:
            logger.warning(
                "Employee %s not found for deletion",
                e.employee_id
            )
            raise HTTPException(404, "Employee not found")

        logger.info(
            "Employee %s deleted successfully",
            e.employee_id
        )

        return {"message": "Employee deleted"}

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Unexpected error while deleting employee %s",
            e.employee_id
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to delete employee"
        )


def get_employee_controller(employee_id: int):
    try:
        employee = repo.get_employee(employee_id)

        if not employee:
            logger.warning(
                "Employee %s not found",
                employee_id
            )
            raise HTTPException(404, "Employee not found")

        logger.info(
            "Employee %s retrieved successfully",
            employee_id
        )

        return employee

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Unexpected error while retrieving employee %s",
            employee_id
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve employee"
        )


def get_all_employees_controller():
    try:
        employees = repo.get_all_employees()

        logger.info(
            "Retrieved %s employees",
            len(employees)
        )

        return employees

    except Exception:
        logger.exception("Unexpected error while retrieving employees")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve employees"
        )