#!/bin/bash

echo "📦 Instalando dependências Python..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/app/requirements.txt

echo "📦 Instalando dependências Node.js..."
cd frontend
npm install
cd ..

echo "🐳 Baixando imagens Docker necessárias..."
docker-compose pull

echo "✅ Setup concluído com sucesso."
