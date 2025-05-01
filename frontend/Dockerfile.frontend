# Dockerfile.frontend

# 1) Base image
FROM node:18-alpine

# 2) Pasta de trabalho
WORKDIR /usr/src/app

# 3) Copia package.json e instala dependências
COPY frontend/package*.json ./
RUN npm install

# 4) Monta o código-fonte
COPY frontend/ .

# 5) Expõe a porta do Vite (5173) e inicia o dev server
EXPOSE 5173
CMD ["npm", "run", "dev"]
