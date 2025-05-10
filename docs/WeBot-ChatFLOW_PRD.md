# Product Requirements Document (PRD)

## 1. Visão Geral  
**WeBot-ChatFLOW** é uma plataforma de suporte multicanal focada no envio e recebimento de e-mails em tempo real, agrupamento automático de conversas e editor rich-text colaborativo. :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}

## 2. Objetivos  
- Prover interface web responsiva para agentes de suporte.  
- Reduzir tempo de resposta via notificações instantâneas.  
- Garantir alta disponibilidade e escalabilidade. :contentReference[oaicite:2]{index=2}:contentReference[oaicite:3]{index=3}

## 3. Requisitos Funcionais  
1. **Envio de e-mail em tempo real** via WebSocket. :contentReference[oaicite:4]{index=4}:contentReference[oaicite:5]{index=5}  
2. **Recebimento e agrupamento** automático de mensagens por `id_conversa`. :contentReference[oaicite:6]{index=6}:contentReference[oaicite:7]{index=7}  
3. **Editor rich-text** com formatação e anexos. :contentReference[oaicite:8]{index=8}:contentReference[oaicite:9]{index=9}  
4. **Autenticação** OAuth2/JWT para todas as rotas protegidas. :contentReference[oaicite:10]{index=10}:contentReference[oaicite:11]{index=11}  
5. **Notificações push** e badge de novas mensagens. :contentReference[oaicite:12]{index=12}:contentReference[oaicite:13]{index=13}  

## 4. Requisitos Não Funcionais  
- **Escalabilidade horizontal** suportada por Kubernetes (staging/prod). :contentReference[oaicite:14]{index=14}:contentReference[oaicite:15]{index=15}  
- **Tempo de latência** máximo de 100 ms no canal WebSocket.  
- **99,9% de disponibilidade** no período de produção.  
- **TLS obrigatório** em todos os ambientes. :contentReference[oaicite:16]{index=16}:contentReference[oaicite:17]{index=17}  

## 5. Restrições  
- Uso de **Docker Compose** em dev e staging; **K8s** em produção. :contentReference[oaicite:18]{index=18}:contentReference[oaicite:19]{index=19}  
- Banco de dados principal: **Postgres**; cache e filas: **Redis**. :contentReference[oaicite:20]{index=20}:contentReference[oaicite:21]{index=21}  
