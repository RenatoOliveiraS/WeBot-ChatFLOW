import os

from app.api.v1.routes.auth_routes import router as auth_router
from app.api.v1.routes.user_routes import router as user_router
from app.core.exception_handlers import (
    authentication_exception_handler,
    business_exception_handler,
    duplicate_exception_handler,
    not_found_exception_handler,
    unauthorized_exception_handler,
    validation_exception_handler,
)
from app.core.exceptions import (
    AuthenticationError,
    BusinessError,
    DuplicateError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)
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

# Registra os handlers de exceção
app.add_exception_handler(AuthenticationError, authentication_exception_handler)
app.add_exception_handler(BusinessError, business_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(NotFoundError, not_found_exception_handler)
app.add_exception_handler(DuplicateError, duplicate_exception_handler)
app.add_exception_handler(UnauthorizedError, unauthorized_exception_handler)

# Inclui as rotas da API
app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"status": "API online"}
