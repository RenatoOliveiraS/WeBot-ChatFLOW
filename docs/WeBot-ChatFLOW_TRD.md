# Technical Reference Document (TRD)

## 1. Endpoints REST & WebSocket

### 1.1 Autenticação  
- **POST** `/api/v1/auth/login`  
  - Request:  
    ```json
    { "email": "string", "password": "string" }
    ```  
  - Response:  
    ```json
    { "access_token": "string", "token_type": "bearer" }
    ``` :contentReference[oaicite:22]{index=22}:contentReference[oaicite:23]{index=23}

### 1.2 Envio de E-mail (WebSocket)  
- **WS** `ws://<host>/ws/email`  
  - Mensagem de entrada:
    ```json
    { "action": "send_email", "payload": { … } }
    ```
  - Mensagem de saída:
    ```json
    { "status":"ok", "ticket_id": "uuid" }
    ``` :contentReference[oaicite:24]{index=24}:contentReference[oaicite:25]{index=25}

## 2. Contratos de Dados  
- **Ticket**: `{ id, subject, participants, status, created_at }`  
- **Email**: `{ id_email, assunto, corpo, remetente, destinatario, id_conversa }` :contentReference[oaicite:26]{index=26}:contentReference[oaicite:27]{index=27}  

## 3. Variáveis de Ambiente Críticas  
| Variável         | Descrição                                |
|------------------|------------------------------------------|
| DATABASE_URL     | String de conexão Postgres               |
| REDIS_URL        | URL de conexão Redis                     |
| SECRET_KEY       | Chave para JWT                           |
| API_BASE_URL     | URL base do front-end (`localhost:3000`) | :contentReference[oaicite:28]{index=28}:contentReference[oaicite:29]{index=29}  
