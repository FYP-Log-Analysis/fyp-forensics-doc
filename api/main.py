from fastapi import FastAPI
from api.routes import pipeline

# Create the FastAPI application
app = FastAPI(
    title="Log Analysis API",
    description="test",
    version="1.0"
)

# Pipeline routes
app.include_router(pipeline.router, prefix="/api/pipeline")
