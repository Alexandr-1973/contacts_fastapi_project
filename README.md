# contacts_fastapi_project

An API project for managing contacts built with **FastAPI**, **asynchronous SQLAlchemy**, and **PostgreSQL**.  
Uses **Redis** for rate limiting, **Alembic** for database migrations, and **Sphinx** for documentation generation.

---

## Tech Stack

- **FastAPI** – high-performance web framework for building APIs  
- **Async SQLAlchemy** + **PostgreSQL** – async database layer  
- **Alembic** – database migrations  
- **Redis** + `fastapi-limiter` – rate limiting  
- **Poetry** – dependency and environment management  
- **Sphinx** – documentation  
- **Python 3.12**

---

## API Documentation

FastAPI automatically generates interactive API docs:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

You can explore and test all available endpoints directly from your browser.

---

## 🧩 Main Commands

> Or, if not using `poetry shell`, prefix commands with `poetry run`, for example:  
> `poetry run uvicorn fastapi_project.main:app --reload`


### 1. Start services with Docker Compose (from project root)

```bash
docker-compose -f ./fastapi_project/src/docker-compose.yml up
```

---

### 2. Run Alembic migrations (from project root)

Create a new migration:

```bash
alembic -c fastapi_project/alembic.ini revision --autogenerate -m "Init"
```

Apply migrations:

```bash
alembic -c fastapi_project/alembic.ini upgrade head
```

---

### 3. Start FastAPI app (from project root)

```bash
uvicorn fastapi_project.main:app --reload
```

---

### 4. Build documentation with Sphinx (from `docs` folder)

```bash
SPHINX_BUILD=1 make html
```

Then open:

```bash
open _build/html/index.html
```

---

### 5. Run tests with Pytest (from project root)

Single test file:

```bash
pytest fastapi_project/tests/test_route_auth.py -W ignore::DeprecationWarning
```

All tests:

```bash
pytest -W ignore::DeprecationWarning
```

With coverage report:

```bash
pytest --cov=fastapi_project/tests/ -W ignore::DeprecationWarning
```

---