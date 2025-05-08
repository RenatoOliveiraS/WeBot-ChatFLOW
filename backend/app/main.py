import os

from app.api.v1.routes.auth_routes import router as auth_router
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Carrega as variáveis de ambiente
load_dotenv()

app = FastAPI(
    title="WeBot ChatFLOW API",
    description="API para o sistema WeBot ChatFLOW",
    version="1.0.0",
)

# Configuração do CORS
cors_origins = os.getenv("CORS_ORIGINS", "").split(",")
if not cors_origins or cors_origins[0] == "":
    cors_origins = ["*"]  # Fallback para desenvolvimento

print("CORS Origins configurados:", cors_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,  # Não exigir credenciais
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas da API
app.include_router(auth_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"status": "API online"}
