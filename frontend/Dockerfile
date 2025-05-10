# 1) Imagem base
FROM node:22-alpine

# 2) Define pasta de trabalho
WORKDIR /usr/src/app

# 3) Garante que estamos em dev e limpa config production
ENV NODE_ENV=development
RUN npm config delete production

# 4) Copia apenas package.json e package-lock.json
COPY package.json package-lock.json ./

# 5) Instala ABSOLUTAMENTE tudo (incluindo devDependencies)
RUN npm ci --include=dev

# 6) Copia todo o código-fonte
COPY . .

# 7) Porta do Vite
EXPOSE 5173

# 8) Inicia o servidor de dev, expondo em 0.0.0.0
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
