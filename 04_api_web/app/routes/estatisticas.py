from fastapi import APIRouter
from app.services.estatisticas_service import obter_estatisticas

router = APIRouter(prefix="/api", tags=["Estatísticas"])


@router.get("/estatisticas")
def get_estatisticas():
    return obter_estatisticas()
