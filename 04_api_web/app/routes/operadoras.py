from fastapi import APIRouter, Query, HTTPException
from app.services.operadoras_service import (
    listar_operadoras,
    buscar_operadora_por_cnpj,
    listar_despesas_por_cnpj
)

router = APIRouter(prefix="/api/operadoras", tags=["Operadoras"])

@router.get("")
def get_operadoras(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    return listar_operadoras(page=page, limit=limit)

@router.get("/{cnpj}")
def get_operadora(cnpj: str):
    operadora = buscar_operadora_por_cnpj(cnpj)

    if not operadora:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")

    return operadora

@router.get("/{cnpj}/despesas")
def get_despesas_operadora(cnpj: str):
    despesas = listar_despesas_por_cnpj(cnpj)

    if not despesas:
        raise HTTPException(
            status_code=404,
            detail="Despesas não encontradas para esta operadora"
        )

    return {
        "cnpj": cnpj,
        "total_registros": len(despesas),
        "despesas": despesas
    }
