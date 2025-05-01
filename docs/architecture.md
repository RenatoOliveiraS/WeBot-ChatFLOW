# Arquitetura de Ambientes

Este documento descreve a arquitetura dos três ambientes do projeto WeBot-ChatFLOW: **development**, **staging** e **production**. Aqui estão os objetivos e componentes principais de cada um, além de diagramas e exemplos de configuração.

---

## 1. Objetivos por ambiente

| Ambiente     | Objetivo principal                                        | Perfis de segurança e compliance           |
|--------------|-----------------------------------------------------------|--------------------------------------------|
| development  | Rápida iteração local, debug e testes unitários           | Acesso aberto (localhost), sem dados reais |
| staging      | Testes de integração com dados próximos da produção       | Acesso restrito (VPN ou IP allowlist)      |
| production   | Serviço em escala, alta disponibilidade e monitoramento   | TLS obrigatório, WAF, backups diários      |

---

## 2. Componentes e recursos

| Componente      | Imagem base                  | Recursos mínimos (CPU/RAM) | Variáveis de ambiente críticas            |
|-----------------|------------------------------|----------------------------|-------------------------------------------|
| **backend**     | `python:3.11-slim`           | 0.5 vCPU / 512 MiB         | `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY` |
| **frontend**    | `node:18-alpine`             | 0.2 vCPU / 256 MiB         | `API_BASE_URL`                            |
| **MySQL**       | `mysql:8.0`                  | 0.5 vCPU / 512 MiB         | `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`   |
| **Redis**       | `redis:7-alpine`             | 0.2 vCPU / 256 MiB         | —                                         |
| **(opcional)**  | RabbitMQ, MinIO, …           | conforme uso               | conforme serviço                          |

---

## 3. Diagrama de Componentes

```mermaid
graph LR
  subgraph App
    FE["Frontend\n(React/Vite)"]
    BE["Backend\n(FastAPI)"]
  end

  FE -->|REST / WebSocket| BE
  BE --> MySQL
  BE --> Redis

  click MySQL "https://hub.docker.com/_/mysql" "MySQL Docker"
  click Redis "https://hub.docker.com/_/redis" "Redis Docker"

```
---

## 4. Diagrama de Deployment

```mermaid
graph TB
  subgraph "Dev (localhost)"
    direction TB
    Compose["Docker Compose"]
    Compose --> BE_dev["Backend"]
    Compose --> FE_dev["Frontend"]
    Compose --> DB_dev["MySQL"]
    Compose --> Cache_dev["Redis"]
  end

  subgraph "Stg (k8s / VM)"
    direction TB
    LB_stg["Load Balancer"]
    BE_stg["Backend Pod"]
    FE_stg["Frontend Pod"]
    DB_stg["MySQL StatefulSet"]
    Cache_stg["Redis Deployment"]
    LB_stg --> BE_stg
    LB_stg --> FE_stg
    BE_stg --> DB_stg
    BE_stg --> Cache_stg
  end

  subgraph "Prod (k8s / Cloud)"
    direction TB
    LB_prd["Load Balancer"]
    BE_prd["Backend ReplicaSet"]
    FE_prd["Frontend ReplicaSet"]
    DB_prd["MySQL Cluster"]
    Cache_prd["Redis Cluster"]
    Mon["Monitoring / Logs"]
    LB_prd --> BE_prd
    LB_prd --> FE_prd
    BE_prd --> DB_prd
    BE_prd --> Cache_prd
    Mon --> BE_prd
    Mon --> FE_prd
    Mon --> DB_prd
    Mon --> Cache_prd
  end
```