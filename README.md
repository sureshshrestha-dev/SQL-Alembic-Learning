# Multi-Tenant Django Learning Project

This project is a Django learning app for a multi-tenant SaaS style system.

The architecture is:

- Tenant -> Department -> User -> Todo
- Each tenant owns its own departments, users, and tasks
- Users are restricted to their tenant
- Roles control what a user is allowed to do

## Stack

- Django
- Django REST Framework
- drf-spectacular
- JWT authentication
- SQLite for local development

## Project structure

```text
config/
  settings.py
  urls.py

tenants/
  models.py
  views.py
  serializers.py
  urls.py

departments/
  models.py
  views.py
  serializers.py
  urls.py

users/
  models.py
  views.py
  serializers.py
  urls.py

todos/
  models.py
  views.py
  serializers.py
  urls.py
```

## Business rules

### Tenant
- A tenant is the top-level organization
- Every user belongs to exactly one tenant
- Every department belongs to exactly one tenant
- Every todo belongs to exactly one tenant

### Roles
- Admin
  - can manage the tenant
  - can create departments
  - can create users in the tenant
  - can see all tenant data
- Supervisor
  - can manage only their own department
  - can assign tasks inside that department
- Agent
  - can only see tasks assigned to themselves
  - can only create tasks in their own department
  - can only assign tasks to themselves

## Local setup

```bash
cd /home/personal/Desktop/learning/SQL-Alembic-Learning
python -m venv .venv
source .venv/bin/activate
pip install -r req.txt
python manage.py migrate
python manage.py runserver
```

If you want a superuser:

```bash
python manage.py createsuperuser
```

## Swagger / API docs

The project includes Swagger via drf-spectacular.

Open:

- http://127.0.0.1:8000/api/schema/
- http://127.0.0.1:8000/swagger/

## Core endpoints

### Auth

```bash
POST /register/
POST /login/
GET /me/
POST /logout/
```

Example register payload:

```json
{
  "username": "admin1",
  "email": "admin1@example.com",
  "password": "secret123",
  "role": "admin"
}
```

Example login payload:

```json
{
  "username": "admin1",
  "password": "secret123"
}
```

### Users

```bash
GET /users/
POST /users/
GET /users/<id>/
PUT /users/<id>/
DELETE /users/<id>/
```

Only tenant admins can create/update users.

### Departments

```bash
GET /departments/
POST /departments/
GET /departments/<id>/
PUT /departments/<id>/
DELETE /departments/<id>/
```

Only tenant admins can create or modify departments.

### Todos

```bash
GET /todos/
POST /todos/
GET /todos/<id>/
PUT /todos/<id>/
DELETE /todos/<id>/
```

Todo access is filtered by tenant and role.

## Example todo payload

```json
{
  "title": "Follow up with customer",
  "description": "Check the invoice status",
  "department": 1,
  "assigned_to": 3,
  "is_completed": false
}
```

## Learning flow

1. Start with tenants
2. Create departments inside a tenant
3. Create users and assign them to a department
4. Make tasks for a tenant and department
5. Add role-based permission checks
6. Test with Swagger and Django test cases

## Security pattern used in this project

For every write route:

- require authentication
- get the tenant from the logged-in user
- reject tenant values that do not match the current user
- validate department ownership
- restrict actions based on role

This is the key idea behind a safe multi-tenant application.

## Notes

This project is intentionally built for learning and experimentation. It is not a production-ready SaaS system, but it demonstrates the right structure and common patterns used in real multi-tenant Django apps.

The main goal is to understand how tenant isolation, department boundaries, user roles, and task ownership work together in a real backend API.
