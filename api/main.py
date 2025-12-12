from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from routes.logs import router as logs_router

# Connection string to the Postgres container defined in docker-compose.
# "db" is the service name, so the hostname resolves inside the Docker network.
DATABASE_URL = "postgresql://forensic:forensicpass@db:5432/fyp"

# Create a SQLAlchemy engine for talking to Postgres.
engine = create_engine(DATABASE_URL)
# Session factory: each request should use its own session from this factory.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base class for ORM models; other files can import this to define tables.
Base = declarative_base()

# Dependency for FastAPI routes to get a DB session.
# Opens a session for the request and ensures it closes afterwards.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app metadata shown in docs and OpenAPI.
app = FastAPI(
    title="Forensics API",
    version="1.0.0",
    description="API for logs"
)

# Mount the logs router under /api/logs.
app.include_router(logs_router, prefix="/api/logs")

# Simple health route to confirm the API is running.
@app.get("/")
def root():
    return {"status": "running", "routes": ["/api/logs"]}
