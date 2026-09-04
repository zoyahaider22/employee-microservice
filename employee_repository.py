import sqlite3
from datetime import datetime
import logging


logger = logging.getLogger(__name__)

DB = "employee.db"


def get_connection():
    try:
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row

        logger.info("Database connection established")

        return conn

    except sqlite3.Error:
        logger.exception("Failed to connect to employee database")
        raise


def init_db():
    conn = None

    try:
        conn = get_connection()
        conn.execute("PRAGMA foreign_keys = ON")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                address TEXT NOT NULL,
                aadhar_number TEXT UNIQUE NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                date_of_joining TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # migration: adds the column if this employees table already
        # existed before date_of_joining was introduced
        try:
            conn.execute("ALTER TABLE employees ADD COLUMN date_of_joining TEXT")
            logger.info("Added date_of_joining column to employees table")
        except sqlite3.OperationalError:
            pass  # column already exists

        conn.execute("""
            CREATE TABLE IF NOT EXISTS leaves (
                leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                financial_year TEXT NOT NULL,
                sick_leave INTEGER NOT NULL DEFAULT 12,
                casual_leave INTEGER NOT NULL DEFAULT 12,
                sick_leave_taken INTEGER NOT NULL DEFAULT 0,
                casual_leave_taken INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
                UNIQUE(employee_id, financial_year)
            )
        """)

        conn.commit()

        logger.info("Employee database initialized successfully")

    except sqlite3.Error:
        logger.exception("Failed to initialize employee database")
        raise

    finally:
        if conn is not None:
            conn.close()


def email_exists(email: str) -> bool:
    conn = None

    try:
        conn = get_connection()

        row = conn.execute(
            "SELECT 1 FROM employees WHERE email=?",
            (email,)
        ).fetchone()

        return row is not None

    except sqlite3.Error:
        logger.exception(
            "Database error while checking email"
        )
        raise

    finally:
        if conn is not None:
            conn.close()


def aadhar_exists(aadhar_number: str) -> bool:
    conn = None

    try:
        conn = get_connection()

        row = conn.execute(
            "SELECT 1 FROM employees WHERE aadhar_number=?",
            (aadhar_number,)
        ).fetchone()

        return row is not None

    except sqlite3.Error:
        logger.exception(
            "Database error while checking Aadhar number"
        )
        raise

    finally:
        if conn is not None:
            conn.close()


def add_employee(
    email, name, age, address, aadhar_number, status,
    date_of_joining=None
) -> int:
    conn = None
    try:
        now = datetime.utcnow().isoformat()
        conn = get_connection()

        cur = conn.execute(
            """
            INSERT INTO employees
            (email, name, age, address, aadhar_number, status,
             date_of_joining, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (email, name, age, address, aadhar_number, status,
             date_of_joining, now, now),
        )
        conn.commit()
        new_id = cur.lastrowid
        logger.info("Employee %s inserted into database", new_id)
        return new_id

    except sqlite3.IntegrityError:
        logger.exception("Database integrity error while adding employee")
        raise
    except sqlite3.Error:
        logger.exception("Database error while adding employee")
        raise
    finally:
        if conn is not None:
            conn.close()

def get_employee(employee_id: int):
    conn = None

    try:
        conn = get_connection()

        row = conn.execute(
            "SELECT * FROM employees WHERE employee_id=?",
            (employee_id,)
        ).fetchone()

        if row:
            logger.info(
                "Employee %s retrieved from database",
                employee_id
            )
            return dict(row)

        logger.warning(
            "Employee %s not found in database",
            employee_id
        )

        return None

    except sqlite3.Error:
        logger.exception(
            "Database error while retrieving employee %s",
            employee_id
        )
        raise

    finally:
        if conn is not None:
            conn.close()


def get_all_employees():
    conn = None

    try:
        conn = get_connection()

        rows = conn.execute(
            "SELECT * FROM employees"
        ).fetchall()

        logger.info(
            "Retrieved %s employees from database",
            len(rows)
        )

        return [dict(r) for r in rows]

    except sqlite3.Error:
        logger.exception(
            "Database error while retrieving all employees"
        )
        raise

    finally:
        if conn is not None:
            conn.close()


def update_employee(
    employee_id, email, name, age, address, aadhar_number, status,
    date_of_joining=None
) -> bool:
    conn = None
    try:
        existing = get_employee(employee_id)
        if not existing:
            logger.warning("Employee %s not found for update", employee_id)
            return False

        conn = get_connection()
        conn.execute(
            """
            UPDATE employees
            SET email=?, name=?, age=?, address=?, aadhar_number=?,
                status=?, date_of_joining=?, updated_at=?
            WHERE employee_id=?
            """,
            (
                email or existing["email"],
                name or existing["name"],
                age or existing["age"],
                address or existing["address"],
                aadhar_number or existing["aadhar_number"],
                status or existing["status"],
                date_of_joining or existing["date_of_joining"],
                datetime.utcnow().isoformat(),
                employee_id,
            ),
        )
        conn.commit()
        logger.info("Employee %s updated in database", employee_id)
        return True

    except sqlite3.IntegrityError:
        logger.exception("Database integrity error while updating employee %s", employee_id)
        raise
    except sqlite3.Error:
        logger.exception("Database error while updating employee %s", employee_id)
        raise
    finally:
        if conn is not None:
            conn.close()


def delete_employee(employee_id: int) -> bool:
    conn = None

    try:
        if not get_employee(employee_id):
            logger.warning(
                "Employee %s not found for deletion",
                employee_id
            )
            return False

        conn = get_connection()

        conn.execute(
            "DELETE FROM employees WHERE employee_id=?",
            (employee_id,)
        )

        conn.commit()

        logger.info(
            "Employee %s deleted from database",
            employee_id
        )

        return True

    except sqlite3.Error:
        logger.exception(
            "Database error while deleting employee %s",
            employee_id
        )
        raise

    finally:
        if conn is not None:
            conn.close()

def add_leave(
    employee_id, financial_year,
    sick_leave=12, casual_leave=12,
    sick_leave_taken=0, casual_leave_taken=0
) -> int:
    conn = None
    try:
        conn = get_connection()
        conn.execute("PRAGMA foreign_keys = ON")

        cur = conn.execute(
            """
            INSERT INTO leaves
            (employee_id, financial_year, sick_leave, casual_leave,
             sick_leave_taken, casual_leave_taken)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (employee_id, financial_year, sick_leave, casual_leave,
             sick_leave_taken, casual_leave_taken),
        )
        conn.commit()
        new_id = cur.lastrowid
        logger.info(
            "Leave record %s created for employee %s (FY %s)",
            new_id, employee_id, financial_year
        )
        return new_id

    except sqlite3.IntegrityError:
        logger.exception(
            "Database integrity error while adding leave for employee %s",
            employee_id
        )
        raise
    except sqlite3.Error:
        logger.exception(
            "Database error while adding leave for employee %s", employee_id
        )
        raise
    finally:
        if conn is not None:
            conn.close()


def get_employee_with_leaves(employee_id: int):
    """
    LEFT OUTER JOIN: employee is returned even with zero leave
    records (leave fields come back as null). Returns None only
    if the employee_id itself doesn't exist.
    """
    conn = None
    try:
        conn = get_connection()

        rows = conn.execute(
            """
            SELECT
                e.employee_id, e.name, e.email, e.date_of_joining,
                l.financial_year, l.sick_leave, l.casual_leave,
                l.sick_leave_taken, l.casual_leave_taken
            FROM employees e
            LEFT JOIN leaves l ON e.employee_id = l.employee_id
            WHERE e.employee_id = ?
            """,
            (employee_id,)
        ).fetchall()

        if not rows:
            logger.warning("Employee %s not found for leave lookup", employee_id)
            return None

        result = {
            "employee_id": rows[0]["employee_id"],
            "name": rows[0]["name"],
            "email": rows[0]["email"],
            "date_of_joining": rows[0]["date_of_joining"],
            "leaves": []
        }

        for row in rows:
            if row["financial_year"] is not None:
                result["leaves"].append({
                    "financial_year": row["financial_year"],
                    "sick_leave": row["sick_leave"],
                    "casual_leave": row["casual_leave"],
                    "sick_leave_taken": row["sick_leave_taken"],
                    "casual_leave_taken": row["casual_leave_taken"],
                })

        logger.info(
            "Retrieved leave details for employee %s (%s records)",
            employee_id, len(result["leaves"])
        )
        return result

    except sqlite3.Error:
        logger.exception(
            "Database error while retrieving leaves for employee %s", employee_id
        )
        raise
    finally:
        if conn is not None:
            conn.close()