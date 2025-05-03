# 📘 Anotações Úteis – Projeto Python com Git

---

## ✅ Comandos Básicos para Projeto Python com Git

### 1. Ativar Ambiente Virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 2. Adicionar Alterações:
```bash
git add .
```

### 3. Comitar Alterações:
```bash
git commit -m "mensagem do commit"
```

### 4. Configurar branch para push (apenas no primeiro push):
```bash
git push -u origin main
```

---

## ⚙️ Comandos Úteis para Rodar o Projeto

### Rodar a aplicação com Uvicorn:

```bash
# Caminho absoluto (se app estiver em src/)
cd src
uvicorn main:app

# Caminho relativo com hot reload (útil no dev)
uvicorn api:app --reload --port 8000
```

---

## 💡 Dica rápida sobre prefixos de commits (`conventional commits`)

| Prefixo   | Quando usar                                                                      |
|-----------|----------------------------------------------------------------------------------|
| `feat`    | Adiciona uma funcionalidade nova ou melhora a experiência do usuário             |
| `fix`     | Corrige um bug ou erro                                                           |
| `refactor`| Muda a estrutura do código sem alterar o comportamento                           |
| `style`   | Ajustes visuais ou de formatação (sem alterar lógica)                            |
| `chore`   | Tarefas auxiliares: build, scripts, CI/CD                                        |

---

## 📦 Gerenciamento de Dependências com `pip`

### Instalar dependências:
```bash
pip install -r requirements.txt
```

### Salvar dependências instaladas:
```bash
pip freeze > requirements.txt
```

---

## 🌱 Gerenciamento de Branches

### Criar e entrar numa nova branch:
```bash
git switch -c nome-da-branch
```

### Entrar em uma branch existente:
```bash
git switch nome-da-branch
```

---

## 🧠 Boas práticas de nomeação de branches

Use um padrão consistente, por exemplo:

```text
feature/a-05-nome-descritivo
fix/login-error
chore/docs-readme
```

**Regras:**
- Use prefixos claros: `feature/`, `fix/`, `chore/`
- Separe escopo e descrição com barras `/` e palavras com hifens `-`
- Inclua o ID da tarefa/jira/story se existir (ex: `a-05`, `b-12`)

---

# 🧪 Utilitários de Testes – Pytest (backend) & Jest (frontend)

---

## ✅ Objetivo

Executar testes automatizados para validação básica (smoke tests) tanto no backend quanto no frontend.

---

## 🐍 Backend – Pytest (Python)

### 🔧 Requisitos

- `pytest` listado no `requirements.txt`:

```txt
pytest
```

### ▶️ Rodar os testes:

```bash
docker-compose exec backend pytest
```

### 💬 Resultado esperado:

Exemplo:

```
collected 1 item
tests/test_placeholder.py .  [100%]
1 passed in 0.25s
```

### 🔍 Opções úteis:

- Mostrar erros completos e ignorar warnings:
```bash
docker-compose exec backend pytest -v --disable-warnings
```

---

## ⚛️ Frontend – Jest (JavaScript/Node)

### 🔧 Requisitos

- Jest já instalado no projeto (`package.json`)
- Pasta típica de testes: `src/__tests__/`

### ▶️ Rodar os testes:

```bash
cd frontend
npm install   # se necessário
npm run test
```

### 💬 Resultado esperado:

Exemplo:

```
Test Suites: 1 passed, 1 total
Tests:       1 passed, 1 total
Snapshots:   0 total
```

---