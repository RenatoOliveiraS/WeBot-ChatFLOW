# Functional Requirements Document (FRD)

## 1. Fluxo de Login  
1. Usuário acessa `/login`.  
2. Front envia **POST** `/api/v1/auth/login`.  
3. Backend valida credenciais e retorna JWT.  
4. Front armazena token e redireciona para dashboard. :contentReference[oaicite:30]{index=30}:contentReference[oaicite:31]{index=31} :contentReference[oaicite:32]{index=32}:contentReference[oaicite:33]{index=33}

## 2. Envio de E-mail  
1. Agente preenche editor rich-text.  
2. Cliente WebSocket envia payload `send_email`.  
3. Backend persiste `Ticket` e `Email`, publica evento em Redis Stream.  
4. Front recebe confirmação e atualiza lista de conversas. :contentReference[oaicite:34]{index=34}:contentReference[oaicite:35]{index=35}

## 3. Recebimento e Agrupamento  
1. Serviço consome Redis Stream de `email_received`.  
2. Identifica `id_conversa`, persiste nova mensagem.  
3. Notifica front via WebSocket `new_message`.  
4. Atualiza badge e marcações de “não lido”. :contentReference[oaicite:36]{index=36}:contentReference[oaicite:37]{index=37}

## 4. Pós-resposta e Arquivamento  
1. Agente clica em “arquivar” no UI.  
2. Backend atualiza `status_conversa = arquivado`.  
3. Front move conversa para lista de arquivados.
