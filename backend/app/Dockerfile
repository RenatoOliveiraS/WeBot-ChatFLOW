# Dockerfile.backend (na raiz)

FROM python:3.11-slim
WORKDIR /app

# 1) Dependências de SO
RUN apt-get update \
  && apt-get install -y --no-install-recommends gcc libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# 2) Dependências Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Código da aplicação — aqui você vai “desempacotar” o app direto em /app
COPY backend/app/ .

# 4) Porta e inicialização
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
