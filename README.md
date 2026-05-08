LeanStock Backend Project

Description:
LeanStock is a backend inventory management system built with FastAPI, PostgreSQL, Redis, SQLModel, and Docker Compose.

The project includes:

User registration and login
JWT authentication
Password hashing with bcrypt
Protected inventory endpoints
Inventory creation
Inventory transfer between locations
Multi-tenant support using tenant_id
PostgreSQL database
Redis integration
Swagger API documentation
TECHNOLOGIES
FastAPI
PostgreSQL
SQLModel
Redis
Docker
Docker Compose
JWT Authentication
Pydantic Validation
PROJECT STRUCTURE

backend/
│
├── app/
│ ├── api/
│ ├── core/
│ ├── models/
│ ├── schemas/
│ ├── services/
│ ├── jobs/
│ └── main.py
│
├── tests/
├── alembic/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.txt

HOW TO RUN THE PROJECT
Install Docker Desktop
Open terminal in project folder
Run the project:

docker compose up --build

Wait until backend starts successfully

You should see:

Application startup complete
Uvicorn running on http://0.0.0.0:8000

SWAGGER DOCUMENTATION

Open browser:

http://localhost:8000/docs

Swagger UI contains all API endpoints and schemas.

AUTHENTICATION FLOW
Register User

POST:
http://localhost:8000/auth/register

Body JSON:

{
"email": "demo@test.com
",
"password": "123456"
}

Login User

POST:
http://localhost:8000/auth/login

Body JSON:

{
"email": "demo@test.com
",
"password": "123456"
}

Response:

{
"access": "JWT_ACCESS_TOKEN",
"refresh": "JWT_REFRESH_TOKEN"
}

Copy access token
Add token to protected requests:

Authorization: Bearer YOUR_ACCESS_TOKEN

INVENTORY ENDPOINTS

Create Inventory Item

POST:
http://localhost:8000/inventory/create

Body JSON:

{
"product_name": "apple",
"location": "A",
"quantity": 20,
"price": 500
}

Transfer Inventory

POST:
http://localhost:8000/inventory/transfer

Body JSON:

{
"product": "apple",
"from_loc": "A",
"to_loc": "B",
"qty": 5
}

Get Inventory List

GET:
http://localhost:8000/inventory/list

Requires Authorization Bearer token.

POSTGRESQL DATABASE

The project uses PostgreSQL database running inside Docker.

Database tables:

user
inventory

Database can be viewed using pgAdmin.

Connection settings:
Host: localhost
Port: 5432
Database: backend
Username: postgres
Password: postgres

SECURITY
Passwords are hashed using bcrypt
JWT access and refresh tokens are implemented
Protected endpoints require Bearer token
Rate limiting uses Redis
CORS configured
No plaintext passwords stored
MULTI-TENANCY

The system uses tenant_id for tenant isolation.

Current project uses mock tenant UUID:

11111111-1111-1111-1111-111111111111

This separates inventory data between different tenants.

HOW TO STOP THE PROJECT

Press:

CTRL + C

Then run:

docker compose down

TESTING

Run tests:

pytest

AUTHOR

Backend project created for backend development laboratory assignment using FastAPI and PostgreSQL.





Update 
pre final project (ENDTERM)

# LeanStock Backend API

LeanStock is a FastAPI backend project for inventory management.

## Features

- User registration
- Email verification
- Login
- JWT access and refresh tokens
- Refresh token rotation
- Logout
- Password reset
- RBAC admin endpoint
- Inventory creation
- Inventory listing with pagination
- Inventory transfer between locations
- Dead stock price decay
- PostgreSQL database
- Redis + Celery background worker
- Email queue
- Docker Compose
- Swagger documentation

## Run Project

```bash
docker compose up --build