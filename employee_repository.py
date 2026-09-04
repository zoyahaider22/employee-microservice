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
    email,
    name,
    age,
    address,
    aadhar_number,
    status
) -> int:

    conn = None

    try:
        now = datetime.utcnow().isoformat()

        conn = get_connection()

        cur = conn.execute(
            """
            INSERT INTO employees
            (
                email,
                name,
                age,
                address,
                aadhar_number,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                email,
                name,
                age,
                address,
                aadhar_number,
                status,
                now,
                now
            ),
        )

        conn.commit()

        new_id = cur.lastrowid

        logger.info(
            "Employee %s inserted into database",
            new_id
        )

        return new_id

    except sqlite3.IntegrityError:
        logger.exception(
            "Database integrity error while adding employee"
        )
        raise

    except sqlite3.Error:
        logger.exception(
            "Database error while adding employee"
        )
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
    employee_id,
    email,
    name,
    age,
    address,
    aadhar_number,
    status
) -> bool:

    conn = None

    try:
        existing = get_employee(employee_id)

        if not existing:
            logger.warning(
                "Employee %s not found for update",
                employee_id
            )
            return False

        conn = get_connection()

        conn.execute(
            """
            UPDATE employees
            SET
                email=?,
                name=?,
                age=?,
                address=?,
                aadhar_number=?,
                status=?,
                updated_at=?
            WHERE employee_id=?
            """,
            (
                email or existing["email"],
                name or existing["name"],
                age or existing["age"],
                address or existing["address"],
                aadhar_number or existing["aadhar_number"],
                status or existing["status"],
                datetime.utcnow().isoformat(),
                employee_id,
            ),
        )

        conn.commit()

        logger.info(
            "Employee %s updated in database",
            employee_id
        )

        return True

    except sqlite3.IntegrityError:
        logger.exception(
            "Database integrity error while updating employee %s",
            employee_id
        )
        raise

    except sqlite3.Error:
        logger.exception(
            "Database error while updating employee %s",
            employee_id
        )
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