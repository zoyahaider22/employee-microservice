from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()

LOG_FILE = "employee_service.log"
MAX_LINES = 200


@router.get("/logs", response_class=PlainTextResponse)
def get_logs():
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        return "".join(lines[-MAX_LINES:])
    except FileNotFoundError:
        return "No logs yet."