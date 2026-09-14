# SQL Alembic Learning

This project is a simple example of using PostgreSQL + SQLAlchemy + Alembic to create tables, track schema changes, and apply migrations.

It includes:
- SQLAlchemy models in `models.py`
- Alembic migration scripts in `alembic/versions/`
- PostgreSQL database connection configured in `alembic.ini`
- Example of creating tables and later altering them with Alembic

## 1. Install dependencies

Create a virtual environment and install the required packages:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r req.txt
```

If you are using `uv`, you can also install from the project metadata:

```bash
uv sync
```

## 2. Install and start PostgreSQL

Make sure PostgreSQL is installed and running locally.

Create a database:

```bash
createdb mydatabase
```

Or with psql:

```bash
psql -U postgres
CREATE DATABASE mydatabase;
\q
```

## 3. Configure the database URL

Open `alembic.ini` and make sure the connection string matches your local PostgreSQL setup:

```ini
sqlalchemy.url = postgresql://postgres:postgres@localhost:5432/mydatabase
```

Update the username, password, host, port, and database name if needed.

## 4. Create the first Alembic migration

Your SQLAlchemy models are defined in `models.py`.

The project is already configured to use `Base.metadata` in `alembic/env.py`, so Alembic can detect model changes.

Generate the first migration script:

```bash
alembic revision --autogenerate -m "initial migration"
```

This will create a migration file in `alembic/versions/` with the SQL commands to create the tables.

## 5. Apply the migration to the database

To create the tables in PostgreSQL:

```bash
alembic upgrade head
```

This runs the migration and creates the tables such as:
- `users`
- `posts`
- `comments`

## 6. Check the database

You can verify the tables were created:

```bash
psql -U postgres -d mydatabase
\dt
```

You should see the tables created by Alembic.

## 7. Make a change after the first migration

When you modify your SQLAlchemy models in `models.py`, for example:
- add a new column,
- rename a column,
- add a new table,
- add a relationship or constraint,

then generate a new migration:

```bash
alembic revision --autogenerate -m "add user status field"
```

Then apply the change:

```bash
alembic upgrade head
```

This is the normal workflow after schema changes.

## 8. Example workflow

```bash
# 1. edit models.py
# 2. create migration
alembic revision --autogenerate -m "add posts and comments tables"

# 3. apply migration
alembic upgrade head
```

## 9. Roll back a migration (optional)

If needed, you can roll back to a previous revision:

```bash
alembic downgrade -1
```

Or go to a specific revision:

```bash
alembic downgrade <revision_id>
```

## 10. Project structure

```text
.
├── alembic/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── alembic.ini
├── models.py
├── pyproject.toml
├── req.txt
└── README.md
```

## 11. Notes

This example uses a local PostgreSQL database and the default Alembic setup:
- `sqlalchemy.url` points to PostgreSQL
- `target_metadata = Base.metadata` allows automatic migration generation
- `alembic upgrade head` applies all pending migrations

This is the basic pattern for a real-world database migration workflow.

## 12. Common commands summary

```bash
# create migration
alembic revision --autogenerate -m "describe change"

# apply all pending migrations
alembic upgrade head

# view migration history
alembic history

# see current migration version
alembic current

# rollback one revision
alembic downgrade -1
```

## Example model used in this project

The project uses SQLAlchemy models with relationships between users, posts, and comments. You can add or update fields there and then generate a migration with Alembic.

This is the standard workflow for a PostgreSQL + Alembic setup: define models, generate a revision, review the script, upgrade the database, and repeat after each schema change.
