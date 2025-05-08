from app.api.v1.controllers.auth_controller import router as auth_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="WeBot API",
    description="API do WeBot - Sistema de Chat Flow",
    version="1.0.0",
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas
app.include_router(auth_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"status": "API online"}
