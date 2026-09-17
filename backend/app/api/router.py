from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.analyze import router as analyze_router
from app.api.project import router as project_router
from app.api.fix import router as fix_router
from app.api.verify import router as verify_router
from app.api.history import router as history_router
from app.api.health import router as health_router
from app.api.error_dna import router as error_dna_router
from app.api.platforms import router as platforms_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(analyze_router)
api_router.include_router(project_router)
api_router.include_router(fix_router)
api_router.include_router(verify_router)
api_router.include_router(history_router)
api_router.include_router(health_router)
api_router.include_router(error_dna_router)
api_router.include_router(platforms_router)
