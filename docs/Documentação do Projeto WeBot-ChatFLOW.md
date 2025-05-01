# **Documentação do Projeto WeBot-ChatFLOW**

## **Sumário**

1. Visão Geral do Projeto

2. Arquitetura do Sistema

3. Estrutura de Pastas

4. Tecnologias e Componentes

5. Fluxos Principais

6. Testes

7. Deploy e CI/CD

8. Padrões de Código e Boas Práticas

9. Roadmap

---

## **1\. Visão Geral do Projeto**

**WeBot-ChatFLOW** é uma plataforma de gestão de conversas multicanal que unifica o envio e recebimento de mensagens (e-mail, WhatsApp, chat interno) em tempo real.

* **Objetivo principal:** Prover um hub centralizado para atendimento ao cliente, facilitando acompanhamento de tickets, histórico de conversas e colaboração entre agentes.

* **Público-alvo:** Equipes de suporte, vendas e relacionamento em empresas de médio e grande porte.

* **Principais funcionalidades:**

  * Envio e recebimento de e-mails em tempo real via WebSocket

  * Agrupamento automático por conversas (“tickets”)

  * Editor rich-text com formatação avançada

  * Autenticação OAuth2/JWT

  * Notificações instantâneas

  * Interface web responsiva (React/TypeScript)

  * Persistência em MySQL, cache e filas em Redis

  * Implantação via Docker e CI/CD

---

## **2\. Arquitetura do Sistema**

Adotamos a **Clean Architecture**, organizando o sistema em quatro camadas concêntricas para isolar regras de negócio de detalhes de infraestrutura.

### **2.1 Camadas e Responsabilidades**

1. **Domain (Entidades)**

   * Modelos de negócio puros (e.g. `Ticket`, `User`), incluindo validações e regras.

2. **Application (Use Cases)**

   * Orquestram as entidades para cada fluxo (e.g. `CreateTicket`, `RespondTicket`).

   * Definem interfaces (ports) para repositórios e gateways.

3. **Interface Adapters**

   * *Controllers* (FastAPI/WebSocket)

   * *Presenters/Serializers*

   * *Port Implementations* (e.g. `TicketRepositoryInterface`)

   * *Adapters de Canais* (e-mail, WhatsApp, interno)

4. **Infrastructure & UI**

   * Implementações concretas de repositórios (MySQL, Redis)

   * Frameworks e clientes (FastAPI, WebSocket, OAuth2/JWT)

   * Scripts de deploy (Docker, Alembic, CI/CD)

### **2.2 Regras de Dependência**

* **Unidirecional:** cada camada depende apenas das internas.

* **Abstrações** (interfaces) residem em camadas interiores; implementações, nas exteriores.

### **2.3 Diagrama de Camadas**
```
mermaid  
graph LR

  subgraph 1.Domain  
    D\[app/domain\]  
  end

  subgraph 2.Application  
    U\[app/use\_cases\]  
  end

  subgraph 3.Interface Adapters  
    R\[app/repositories/interfaces\]  
    A\[app/adapters\]  
  end

  subgraph 4.Infrastructure & UI  
    API\[app/api \+ core\]  
    INFRA\[DB(MySQL), Redis, OAuth2/JWT, Docker, CI/CD\]  
  end

  D \--\> U  
  U \--\> R  
  U \--\> A  
  R \--\> INFRA  
  A \--\> INFRA  
  API \--\> U  
  API \--\> D
```

---

## **3\. Estrutura de Pastas**

Visão física do projeto, já alinhada ao mapeamento de camadas acima:

```
WeBot-ChatFLOW/  
├── frontend/                           \# Novo: projeto React com Vite  
│   ├── vite.config.ts                  \# Configuração do Vite  
│   ├── package.json  
│   └── src/  
│       ├── main.tsx                    \# Entry point React  
│       ├── components/                 \# Componentes React  
│       ├── routes/                     \# Rotas do React Router (se houver)  
│       └── styles/                     \# Estilos globais / CSS Modules  
├── app/  
│   ├── api/                            \# Infrastructure & UI – FastAPI routes e config  
│   │   └── v1/  
│   │       └── routes/  
│   │           ├── ticket\_routes.py  
│   │           ├── user\_routes.py  
│   │           └── channel\_routes.py  
│   ├── core/                           \# Configurações gerais (DB, settings)  
│   │   ├── config.py  
│   │   └── database.py  
│   ├── domain/                         \# Domain – Entidades e schemas puros  
│   │   ├── ticket/  
│   │   │   ├── models.py  
│   │   │   ├── schemas.py  
│   │   │   └── enums.py  
│   │   ├── user/  
│   │   └── channel/  
│   ├── use\_cases/                      \# Application – Casos de uso (ports \+ orquestrações)  
│   │   ├── create\_ticket.py  
│   │   ├── assign\_ticket.py  
│   │   ├── respond\_ticket.py  
│   │   └── channel\_dispatcher.py       \# movido de services → pertence à orquestração  
│   ├── repositories/                   \# Interface Adapters – contratos e implementações  
│   │   ├── interfaces/                 \# → contratos (ports)  
│   │   └── implementations/            \# → MySQL, Redis, etc.  
│   ├── adapters/                       \# Interface Adapters – canais externos  
│   │   ├── email\_channel.py  
│   │   ├── whatsapp\_channel.py  
│   │   └── internal\_channel.py  
│   ├── events/                         \# Infraestrutura – eventos e filas  
│   ├── tests/                          \# Testes unitários e de integração  
│   └── main.py                         \# Ponto de entrada da aplicação  
├── alembic/                            \# Migrations  
├── Dockerfile                          \# Infraestrutura de container  
├── docker-compose.yml  
├── .github/                            \# CI/CD (GitHub Actions)  
├── requirements.txt  
└── .env
```

---

## **4\. Tecnologias e Componentes**

| Camada | Tecnologia / Biblioteca |
| ----- | ----- |
| Front-end UI | Vite \+ React \+ TypeScript, TipTap (rich-text) |
| API / WebSocket | FastAPI, starlette-websockets |
| Domínio | Pydantic, enums |
| Casos de Uso | Python puro, interfaces (ports) |
| Repositórios | SQLAlchemy (MySQL), aioredis |
| Mensageria / Eventos | Redis Streams / Celery |
| Autenticação / Autorização | OAuth2 (Keycloak?), JWT, PyJWT |
| Notificações | WebSocket, push notifications |
| Testes | pytest, pytest-asyncio, Jest |
| Deploy | Docker, docker-compose, AWS/GCP |
| CI/CD | GitHub Actions |

---

## **5\. Fluxos Principais**

### **5.1 Envio de E-mail em Tempo Real**

1. Front-end envia payload ao endpoint WebSocket.

2. Controle (`EmailController`) valida via schemas Pydantic.

3. Caso de uso `CreateTicket` orquestra `Ticket` e `Email` → persistência via `IEmailRepository`.

4. Adapter `SMTPChannel` encaminha mensagem ao servidor de e-mail.

5. Evento `ticket_created` é publicado no Redis Stream.

6. Front-end recebe confirmação e atualiza UI.

### **5.2 Recebimento e Agrupamento por Conversas**

1. Listener consume Redis Stream de eventos de e-mail recebido.

2. Adapter `POP3Channel` ou `IMAPChannel` processa e converte em DTO.

3. Caso de uso `RespondTicket` identifica conversa (`ticket_id`) e armazena resposta.

4. Notificação via WebSocket notifica agentes conectados.

### **5.3 Editor Rich-Text**

* Baseado em TipTap, integrando plugins de formatação, anexos e histórico de versões.

### **5.4 Autenticação OAuth2/JWT**

* Fluxo Authorization Code com Keycloak (ou outro provider).

* Endpoints protegidos por dependência de segurança no FastAPI.

---

## **6\. Testes**

* **Unitários:**

  * `tests/domain/`

  * `tests/use_cases/`

* **Integração:**

  * `tests/api/` (FastAPI TestClient \+ banco em memória)

  * Mocks para Redis e SMTP.

* **Cobertura:**

  * Meta mínima de 90%.

---

## **7\. Deploy e CI/CD**

1. **Docker:**

   * `Dockerfile` separados para front-end e back-end.

   * `docker-compose.yml` orquestra serviços (app, MySQL, Redis).

2. **Migrations:**

   * Alembic para versionamento de schema.

3. **CI/CD (GitHub Actions):**

   * Build, lint (flake8, eslint), testes, coverage report.

   * Publicação de imagens Docker em registry.

   * Deploy automatizado em staging/produção (via Terraform ou Ansible).

---

## **8\. Padrões de Código e Boas Práticas**

* **Clean Architecture** estrita: dependências unidirecionais.

* **Injeção de Dependências:** via factories no `main.py`.

* **Naming Conventions:** snake\_case em Python; PascalCase em TypeScript.

* **Lint e Formatação:** black, isort, eslint, prettier.

* **Documentação de Código:** docstrings conforme PEP-257, OpenAPI para endpoints.

---

## **9\. Roadmap**

* Suporte a canais adicionais (Telegram, Facebook Messenger)

* Dashboard de métricas e relatórios

* Mobile app (React Native)

* IA para sugestão de respostas automáticas

* Internacionalização (i18n)

