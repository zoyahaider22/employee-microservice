import sqlite3
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI()
DB = "employee.db"

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

db().execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    address TEXT NOT NULL,
    aadhar_number TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
)""")

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

@app.post("/add")
def add(e: AddReq):
    conn = db()
    if conn.execute("SELECT 1 FROM employees WHERE email=?", (e.email,)).fetchone():
        raise HTTPException(400, "Email already exists")
    if conn.execute("SELECT 1 FROM employees WHERE aadhar_number=?", (e.aadhar_number,)).fetchone():
        raise HTTPException(400, "Aadhar number already exists")
    now = datetime.utcnow().isoformat()
    cur = conn.execute(
        "INSERT INTO employees (email,name,age,address,aadhar_number,status,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)",
        (e.email, e.name, e.age, e.address, e.aadhar_number, e.status, now, now),
    )
    conn.commit()
    return {"message": "Employee added", "employee_id": cur.lastrowid}

@app.post("/modify")
def modify(e: ModifyReq):
    conn = db()
    row = conn.execute("SELECT * FROM employees WHERE employee_id=?", (e.employee_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Employee not found")
    conn.execute(
        "UPDATE employees SET email=?, name=?, age=?, address=?, aadhar_number=?, status=?, updated_at=? WHERE employee_id=?",
        (
            e.email or row["email"], e.name or row["name"], e.age or row["age"],
            e.address or row["address"], e.aadhar_number or row["aadhar_number"],
            e.status or row["status"], datetime.utcnow().isoformat(), e.employee_id,
        ),
    )
    conn.commit()
    return {"message": "Employee updated"}

@app.post("/delete")
def delete(e: DeleteReq):
    conn = db()
    if not conn.execute("SELECT 1 FROM employees WHERE employee_id=?", (e.employee_id,)).fetchone():
        raise HTTPException(404, "Employee not found")
    conn.execute("DELETE FROM employees WHERE employee_id=?", (e.employee_id,))
    conn.commit()
    return {"message": "Employee deleted"}

@app.get("/employees")
def list_all():
    return [dict(r) for r in db().execute("SELECT * FROM employees").fetchall()]

@app.get("/employees/{employee_id}")
def get_one(employee_id: int):
    row = db().execute("SELECT * FROM employees WHERE employee_id=?", (employee_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Employee not found")
    return dict(row)