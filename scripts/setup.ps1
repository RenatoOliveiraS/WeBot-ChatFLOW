Write-Host "📦 Instalando dependências Python..."
python -m venv venv
./venv/Scripts/Activate.ps1
pip install --upgrade pip
pip install -r backend/app/requirements.txt

Write-Host "📦 Instalando dependências Node.js..."
cd frontend
npm install
cd ..

Write-Host "🐳 Baixando imagens Docker necessárias..."
docker-compose pull

Write-Host "✅ Setup concluído com sucesso."
