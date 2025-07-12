An API project for managing contacts built with FastAPI, asynchronous SQLAlchemy, and PostgreSQL.  
Uses Redis for rate limiting and Alembic for database migrations.  
Documentation is generated with Sphinx.

Tech Stack
    •	FastAPI (REST API)
    •	Async SQLAlchemy + PostgreSQL
    •	Alembic (database migrations)
    •	Redis + fastapi-limiter (rate limiting)
    •	Poetry (dependency and environment management)
    •	Sphinx (documentation)
    •	Python 3.12

API Documentation

FastAPI automatically generates interactive API docs available at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

You can use these interfaces to explore all available endpoints and test them directly from the browser.

Main commands:

start with uvicorn from root (contacts_fastapi_project):

uvicorn fastapi_project.main:app --reload

alembic from root (contacts_fastapi_project):

alembic -c fastapi_project/alembic.ini revision --autogenerate -m "Init"

alembic -c fastapi_project/alembic.ini upgrade head

docker-compose from root (contacts_fastapi_project):

docker-compose -f ./fastapi_project/src/docker-compose.yml up

SPHINX from (contacts_fastapi_project)/docs: 

SPHINX_BUILD=1 make html

pytest from root (contacts_fastapi_project):

pytest fastapi_project/tests/test_route_auth.py -W ignore::DeprecationWarning

pytest -W ignore::DeprecationWarning

pytest --cov=fastapi_project/tests/ -W ignore::DeprecationWarning


# contacts_fastapi_project

An API project for managing contacts built with **FastAPI**, **asynchronous SQLAlchemy**, and **PostgreSQL**.  
Uses **Redis** for rate limiting, **Alembic** for database migrations, and **Sphinx** for documentation generation.

---

## 🚀 Tech Stack

- **FastAPI** – high-performance web framework for building APIs  
- **Async SQLAlchemy** + **PostgreSQL** – async database layer  
- **Alembic** – database migrations  
- **Redis** + `fastapi-limiter` – rate limiting  
- **Poetry** – dependency and environment management  
- **Sphinx** – documentation  
- **Python 3.12**

---

## 📚 API Documentation

FastAPI automatically generates interactive API docs:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

You can explore and test all available endpoints directly from your browser.

---

## 🧩 Main Commands

### ▶️ Run FastAPI app (from project root)

```bash
uvicorn fastapi_project.main:app --reload
```

---

### 🔃 Alembic migrations (from project root)

Create a new migration:

```bash
alembic -c fastapi_project/alembic.ini revision --autogenerate -m "Init"
```

Apply migrations:

```bash
alembic -c fastapi_project/alembic.ini upgrade head
```

---

### 🐳 Run services with Docker Compose (from project root)

```bash
docker-compose -f ./fastapi_project/src/docker-compose.yml up
```

---

### 🛠 Build documentation with Sphinx (from `docs` folder)

```bash
SPHINX_BUILD=1 make html
```

Then open:

```bash
open _build/html/index.html
```

---

### ✅ Run tests with Pytest (from project root)

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

## 🧾 License

MIT License.  
© [Alexandr-1973](https://github.com/Alexandr-1973)