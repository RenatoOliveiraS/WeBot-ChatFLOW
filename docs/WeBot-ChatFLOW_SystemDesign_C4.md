# System Design (C4 Model)

## 1. Context Diagram  
```mermaid
graph LR
  UserAgent[Agente de Suporte]
  System[WeBot-ChatFLOW]
  SMTP[Servidor SMTP]
  IMAP[Servidor IMAP]
  UserAgent -->|HTTP/WS| System
  System --> SMTP
  System --> IMAP
