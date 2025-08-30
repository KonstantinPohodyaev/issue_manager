# 📝 Issue Manager

![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-0?logo=fastapi&logoColor=white&labelColor=009688&color=009688)  
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.40-orange?logo=sqlalchemy)  
![Alembic](https://img.shields.io/badge/Alembic-1.16.4-3796b0?logo=alembic)  
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)  
![pytest](https://img.shields.io/badge/pytest-8.4.1-ff69b4?logo=python)  
![uvicorn](https://img.shields.io/badge/uvicorn-0.35.0-black?logo=fastapi)  

> Test assignment: Task Manager with CRUD operations and tests.

---

## 🚀 Opportunities

### 🧠 Backend (FastAPI + SQLAlchemy + PostgreSQL)
## 🚀 Features

### 🧠 Backend (FastAPI + SQLAlchemy + PostgreSQL/SQLite)

- 📡 Asynchronous FastAPI server with modular structure  
- 📊 Full CRUD operations on tasks  
- 🧩 Business logic:
  - Validate task existence
  - Prevent updates on completed tasks
  - UUID-based unique identification
  - Custom validators for task data

### ⚙️ DevOps & Infrastructure

- 📦 Docker + Docker Compose support  
- 🧾 Alembic for database migrations  
- 🔐 Flexible `poetry` configuration 

---

## ⚙️ Installation

```bash
git clone https://github.com/KonstantinPohodyaev/issue_manager.git
cd issue_manager
```

Install Poetry (if not installed)::

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Active virtual environment:

```bash
cd issue_manager
poetry env activate
# copy your line from terminale like this and press ENTER
# source /Users/kspohodyaev/Library/Caches/pypoetry/virtualenvs/src-w3klOcYr-py3.12/bin/activate
```

Download requirements
```
poetry install
```

### 📦 Configure environment variables in a .env file in the project root:

Create `.env` file in the project root like `.env.example`:

```env
# === DATABASE CONFIGURATION ===
# FastAPI configuration
FASTAPI_TITLE=Issue Manager
FASTAPI_DESCRIPTION=Issue Manager - project for tracking tasks
DEBUG=1

# Production database (PostgreSQL)
DB_DIALECT=postgresql
DB_DRIVER=asyncpg
DB_USER=user
DB_PASSWORD=password
DB_HOST=db
DB_PORT=5432
DB_NAME=db

# Test database (SQLite)
TEST_DB_DIALECT=sqlite
TEST_DB_DRIVER=aiosqlite
TEST_DB_NAME=test_db.db
```
---

## ▶️ Debug start

### Write `DEBUG=1` in `.env`

### Apply migrations
```bash
alembic upgrade head
```

### Start backend-server:

```bash
uvicorn src.main:app --reload
```

_API`s url ```http://127.0.0.1:8000/docs```_

## ▶️ Run in Docker-containers
_Before start your Docker Desktop_

### Write `DEBUG=0` in `.env`

### Run containers:

```bash
docker compose up -d
```

### Apply migrations:

```bash
docker compose exec -it web bash
alembic upgrade head
```

### Остановка контейнеров (flag -v for deleting volumes - Optionally)
```bash
docker compose down -v 
```

_API`s url ```http://127.0.0.1/docs```_

---

## Run testing

### Write `DEBUG=1' in `.env`

### Run
```bash
pytest
```

## 👨‍💻 Author

**Pohodyaev Konstantin**  
Telegram: [@kspohodyaev](https://t.me/kspohodyaev)

---
