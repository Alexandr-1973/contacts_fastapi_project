import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_limiter import FastAPILimiter
from fastapi_project.src.database.db import get_db
from fastapi_project.src.routes import contacts, auth, users
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context for initializing and closing application-level resources.

    This function sets up the Redis connection for FastAPI Limiter and closes it on shutdown.

    :param app: The FastAPI application instance.
    :type app: FastAPI
    """
    r = redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)
    yield
    await r.aclose()

app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix='/api')

@app.get("/")
def index():
    """
    Root endpoint for the application.

    :return: A welcome message.
    :rtype: dict
    """
    return {"message": "Contacts Application"}

@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    Database health check endpoint.

    Verifies that the database is responsive and correctly configured.

    :param db: Dependency that provides an asynchronous database session.
    :type db: AsyncSession
    :raises HTTPException: If the database is not configured properly or not reachable.
    :return: Message confirming the database is operational.
    :rtype: dict
    """
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to Contacts App!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

