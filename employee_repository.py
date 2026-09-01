import sqlite3
from datetime import datetime

DB = "employee.db"


def get_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
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
        )
    """)
    conn.commit()
    conn.close()


def email_exists(email: str) -> bool:
    conn = get_connection()
    row = conn.execute("SELECT 1 FROM employees WHERE email=?", (email,)).fetchone()
    conn.close()
    return row is not None


def aadhar_exists(aadhar_number: str) -> bool:
    conn = get_connection()
    row = conn.execute("SELECT 1 FROM employees WHERE aadhar_number=?", (aadhar_number,)).fetchone()
    conn.close()
    return row is not None


def add_employee(email, name, age, address, aadhar_number, status) -> int:
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO employees (email,name,age,address,aadhar_number,status,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)",
        (email, name, age, address, aadhar_number, status, now, now),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_employee(employee_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM employees WHERE employee_id=?", (employee_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_employees():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM employees").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_employee(employee_id, email, name, age, address, aadhar_number, status) -> bool:
    existing = get_employee(employee_id)
    if not existing:
        return False

    conn = get_connection()
    conn.execute(
        "UPDATE employees SET email=?, name=?, age=?, address=?, aadhar_number=?, status=?, updated_at=? WHERE employee_id=?",
        (
            email or existing["email"], name or existing["name"], age or existing["age"],
            address or existing["address"], aadhar_number or existing["aadhar_number"],
            status or existing["status"], datetime.utcnow().isoformat(), employee_id,
        ),
    )
    conn.commit()
    conn.close()
    return True


def delete_employee(employee_id: int) -> bool:
    if not get_employee(employee_id):
        return False
    conn = get_connection()
    conn.execute("DELETE FROM employees WHERE employee_id=?", (employee_id,))
    conn.commit()
    conn.close()
    return True