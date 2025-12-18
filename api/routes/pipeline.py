from fastapi import APIRouter
from api.services.pipeline_service import run_pipeline

router = APIRouter()

@router.post("/run")
def run_full_pipeline():
    result = run_pipeline()
    return result
