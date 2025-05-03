# 📚 Documentação – Criando Tabelas com SQLAlchemy + Alembic

## 🧱 Pré-requisitos (já feitos):

- Models definidos no diretório `models/`, herdando de `Base` de `core.database`
- Models registrados no `models/__init__.py`
- `env.py` com `import models` (ou similar) para garantir que o Alembic enxergue os models
- Script `docker:migrate` definido no `package.json`:

```json
"scripts": {
  "docker:migrate": "docker-compose exec backend alembic upgrade head"
}
```

---

## ✅ Passos para criar uma nova tabela no banco de dados:

### 1. Criar um novo model

Exemplo: `models/product_model.py`

```python
from sqlalchemy import Column, Integer, String
from core.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
```

---

### 2. Registrar no `models/__init__.py`

```python
from .user_model import User
from .product_model import Product  # <--- novo model
```

---

### 3. Gerar a migration com Alembic

```bash
docker-compose exec backend alembic revision --autogenerate -m "create products table"
```

Verifique o conteúdo gerado em `migrations/versions/` para confirmar que o `op.create_table` está lá.

---

### 4. Aplicar a migration com NPM (executar no banco)

```bash
npm run docker:migrate
```

---

### 5. Validar a criação da tabela

```bash
docker-compose exec postgres psql -U postgres -d webot_chatflow -c "\dt"
```

---

## ✅ Checklist rápido (resumo):

- [ ] Criou o model com `Base`?
- [ ] Registrou no `models/__init__.py`?
- [ ] Rodou `alembic revision --autogenerate`?
- [ ] Rodou `npm run docker:migrate`?
- [ ] Validou com `\dt`?

