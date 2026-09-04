from fastapi import FastAPI
import logging

import employee_repository as repo
from employee_router import router
from logs_router import router as logs_router
from logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI()

repo.init_db()
app.include_router(router)
app.include_router(logs_router)

logger.info("Employee service started")