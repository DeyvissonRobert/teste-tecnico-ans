from fastapi import FastAPI
from app.routes.operadoras import router as operadoras_router
from app.routes.estatisticas import router as estatisticas_router

app = FastAPI(
    title="API ANS",
    description="API para consulta de operadoras e despesas da ANS",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {"status": "ok"}

app.include_router(operadoras_router)
app.include_router(estatisticas_router)
