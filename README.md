# Run Tracker API

A backend REST API built with FastAPI for logging and tracking running sessions. Users can register, log in, and manage their own run history, while admins can view and moderate runs across every account.

## Features

* User registration and JWT based authentication
* Password hashing with bcrypt via passlib
* Role based access control separating regular users from admins
* Full CRUD operations for run entries (create, read, update, delete)
* User profile endpoints for viewing account info, updating phone number, and changing password
* Admin endpoints to view and delete any user's runs
* PostgreSQL database integration through SQLAlchemy ORM
* Alembic configured for database migrations

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic for request validation
* Passlib (bcrypt) for password hashing
* python jose for JWT encoding and decoding
* Alembic for migrations

## Data Models

**Users**
id, email, username, hashed password, active status, role, phone number

**Runs**
id, title, distance in kilometers, duration in minutes, average heart rate, linked to a user through a foreign key

## API Endpoints

**Auth**
POST /auth/createnewuser — register a new user
POST /auth/userlogin — log in and receive a JWT access token
GET /auth/getallusers — list all users
PUT /auth/update_phone_number — update the logged in user's phone number

**User**
GET /user/information — view the logged in user's profile
PUT /user/change_password — change the logged in user's password

**Runs**
POST /createnewrun — log a new run
GET /getallruns — get all runs belonging to the logged in user
GET /get_run_by_id/{run_id} — get a single run by id
PUT /update_run — update an existing run
DELETE /delete_run/{run_id} — delete a run

**Admin**
GET /admin/get_runs_of_every_users — view every user's runs (admin only)
DELETE /admin/to_delete_runs_as_a_admin/{run_id} — delete any run by id (admin only)

## Setup

1. Clone the repository
2. Install dependencies with pip (fastapi, uvicorn, sqlalchemy, psycopg2, passlib, python jose, alembic)
3. Create a PostgreSQL database and update the connection string in database.py
4. Run the Alembic migrations to create the tables
5. Start the server with uvicorn main:app reload
6. Visit /docs for the interactive Swagger UI

## Notes

This project was built to practice authentication, authorization, and relational database design in FastAPI, extending patterns from an earlier workout tracking API into a run specific domain.
