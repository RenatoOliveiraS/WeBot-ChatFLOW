# src/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Session
from src.db import engine
from src.config import settings
from fastapi import HTTPException
from fastapi.responses import FileResponse
import os
import mimetypes
from fastapi.middleware.cors import CORSMiddleware



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def seed_admin_user():
    # importe também os crud de departamentos e cargos
    from src.features.users.crud import (
        get_user_by_email,
        create_user,
        assign_departamento,
        assign_cargo,
    )
    from src.features.departamentos.crud import (
        get_departamento_by_name,
        create_departamento,
    )
    from src.features.cargos.crud import (
        get_cargo_by_name,
        create_cargo,
    )

    if settings.ADMIN_NAME and settings.ADMIN_EMAIL and settings.ADMIN_PASSWORD:
        with Session(engine) as session:
            # 1) Cria ou obtém o usuário admin
            user = get_user_by_email(session, settings.ADMIN_EMAIL)
            if not user:
                user = create_user(
                    session,
                    name=settings.ADMIN_NAME,
                    email=settings.ADMIN_EMAIL,
                    password=settings.ADMIN_PASSWORD
                )

            # 2) Cria ou obtém o departamento “Administrador” e associa
            dept = get_departamento_by_name(session, "Administrador")
            if not dept:
                dept = create_departamento(session, "Administrador")
            assign_departamento(session, user.uuid, dept.id)

            # 3) Cria ou obtém o cargo “Administrador” e associa
            cargo = get_cargo_by_name(session, "Administrador")
            if not cargo:
                cargo = create_cargo(session, "Administrador")
            assign_cargo(session, user.uuid, cargo.id)

def get_app() -> FastAPI:

    app = FastAPI()

    # Configuração do CORS: pega a origem do frontend da variável de ambiente VITE_FRONTEND_URL (ou usa um valor padrão)
    frontend_url = os.getenv("VITE_FRONTEND_URL", "http://localhost:5173")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/attachments/{safe_id}/{filename}")
    def serve_attachment(safe_id: str, filename: str):
        base = getattr(
            settings,
            "INBOUND_EMAIL_ATTACHMENTS_DIR",
            "./attachments/inbound_emails"
        )
        full_path = os.path.join(base, safe_id, filename)
        if not os.path.isfile(full_path):
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        # define Content-Type a partir da extensão
        content_type, _ = mimetypes.guess_type(full_path)
        content_type = content_type or "application/octet-stream"
        # inline para imagens, attachment para o resto
        disposition = "inline" if content_type.startswith("image/") else "attachment"
        headers = {
            "Content-Disposition": f'{disposition}; filename="{filename}"',
            "Cache-Control": "public, max-age=86400"
        }
        return FileResponse(full_path, media_type=content_type, headers=headers)

    # 1) Registra todos os routers primeiro, garantindo que
    #    os módulos de modelo sejam importados (populando SQLModel.metadata)
    import pkgutil, importlib
    from pathlib import Path

    feature_dir = Path(__file__).parent / "features"
    for finder, name, ispkg in pkgutil.iter_modules([str(feature_dir)]):
        mod = importlib.import_module(f"src.features.{name}.router")
        app.include_router(mod.router)

    # 2) Só agora crie as tabelas e rode o seed do admin
    create_db_and_tables()
    seed_admin_user()

    return app

app = get_app()
