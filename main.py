from fastapi import FastAPI
import employee_repository as repo
from employee_router import router

app = FastAPI()

repo.init_db()
app.include_router(router)