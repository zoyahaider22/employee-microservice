# Employee Management API

A RESTful microservice for managing employee data, built with **FastAPI** and **SQLite**, using a layered architecture (router → controller → repository → model).

## Features

- Add, modify, and delete employee records
- Fetch a single employee or the full list
- Automatic validation of incoming data (via Pydantic)
- Enforced uniqueness on email and Aadhar number
- Automatic `created_at` / `updated_at` timestamp tracking

## Tech Stack

- **FastAPI** — web framework
- **SQLite** — database (single file, no separate server required)
- **Pydantic** — request validation

## Architecture

This project is split into layers, each with a single responsibility:

```
Client
  │
  ▼
employee_router.py        → maps API endpoints to controller functions
  │
  ▼
employee_controller.py    → business logic (duplicate checks, existence checks)
  │
  ▼
employee_repository.py    → the only file that talks to the database
  │
  ▼
employee.db (SQLite)
```

| File | Responsibility |
|---|---|
| `employee_model.py` | Defines request shapes (`AddReq`, `ModifyReq`, `DeleteReq`) using Pydantic |
| `employee_repository.py` | All direct database access (SQL queries) |
| `employee_controller.py` | Business logic — decides what should happen, calls the repository |
| `employee_router.py` | Thin layer — maps HTTP endpoints to controller functions |
| `main.py` | Starts the app and wires the router in |

This separation means the database can be swapped out by only changing `employee_repository.py`, without touching the API logic or endpoints at all.

## Employee Fields

| Field | Type | Notes |
|---|---|---|
| `employee_id` | int | Auto-generated, unique |
| `email` | string | Unique |
| `name` | string | |
| `age` | int | |
| `address` | string | |
| `aadhar_number` | string | Unique |
| `status` | string | `active` or `inactive` |
| `created_at` | string | Set once, on creation |
| `updated_at` | string | Refreshed on every modify |

## API Endpoints

All write operations use `POST`, as specified for this assignment.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/add` | Add a new employee |
| `POST` | `/modify` | Update an existing employee (only send fields you want to change) |
| `POST` | `/delete` | Delete an employee by ID |
| `GET` | `/employees` | List all employees |
| `GET` | `/employees/{employee_id}` | Get a single employee by ID |

### Example: Add an employee
```json
POST /add
{
  "email": "rahul@example.com",
  "name": "Rahul",
  "age": 24,
  "address": "Delhi",
  "aadhar_number": "123412341234",
  "status": "active"
}
```

### Example: Modify one field
```json
POST /modify
{
  "employee_id": 1,
  "status": "inactive"
}
```
Only the fields you send are updated — everything else stays unchanged.

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Then open `http://localhost:8001/docs` for interactive API documentation and testing.

## Author

Zoya Haider 