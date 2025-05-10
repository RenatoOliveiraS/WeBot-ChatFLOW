# Engineering Guidelines

## 1. Padrões de Código  
- **Python**: PEP-8, `black --check`, `isort` :contentReference[oaicite:42]{index=42}:contentReference[oaicite:43]{index=43}  
- **JavaScript/TS**: ESLint + Prettier

## 2. Code Review  
- PRs < 300 linhas de diff.  
- Passar pelo menos 2 revisores.  
- Usar `conventional commits` (feat/, fix/, chore/) :contentReference[oaicite:44]{index=44}:contentReference[oaicite:45]{index=45}  

## 3. Testes  
- **Backend**: pytest ≥ 90% coverage.  
- **Frontend**: Jest + React Testing Library.  
- Executar testes em pipeline CI antes do merge. :contentReference[oaicite:46]{index=46}:contentReference[oaicite:47]{index=47}

## 4. CI/CD  
- GitHub Actions: lint → build → testes → deploy staging.  
- Deploy produção manual via tag `v*.*.*`.

## 5. Segurança  
- Revisão de dependências (dependabot/automerge).  
- Auditoria trimestral de bibliotecas.
