# RFC: Integração do WhatsApp como Canal de Suporte

- **Status**: Draft  
- **Autor**: [Seu Nome]  
- **Data**: 2025-05-09  
- **Comentários até**: 2025-05-23

## 1. Contexto  
Atualmente suportamos e-mail, mas muitos clientes preferem WhatsApp para atendimento instantâneo.

## 2. Proposta  
Adicionar um adapter `WhatsAppChannel` usando API oficial do WhatsApp Business, permitindo:
- Envio e recebimento de mensagens.
- Mapear mensagens para tickets existentes.  

## 3. Impacto  
- Nova dependência: `whatsapp-business-api`  
- Ajustes no TRD, FRD e testes.

## 4. Alternativas  
- Usar Twilio Conversations (custo adicional).  
- Manter apenas e-mail e chat interno.  

## 5. Solicito feedback sobre:  
- Segurança e compliance do canal.  
- Performance e escalabilidade.
