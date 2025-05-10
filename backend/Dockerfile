FROM python:3.10-slim

WORKDIR /app

# 1) Dependências de sistema
RUN apt-get update --fix-missing \
 && apt-get install -y --no-install-recommends \
      gcc \
      libpq-dev \
      netcat-openbsd \
      git \
 && rm -rf /var/lib/apt/lists/*

# 2) Instalação de dependências Python
COPY requirements.txt .

# Instala dependências em ordem específica
RUN python -m pip install --upgrade pip \
 && python -m pip install --no-cache-dir cryptography==41.0.7 \
 && python -m pip install --no-cache-dir python-jose[cryptography]==3.3.0 \
 && python -m pip install --no-cache-dir -r requirements.txt \
 && python -m pip install --no-cache-dir alembic

# 3) Copia o código-fonte
COPY . .

# 4) Permissões e entrypoint
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
