# ADR: Uso de Redis para Cache e Filas

## 1. Contexto  
Precisamos melhorar latência e escalar entrega de eventos em múltiplas instâncias. :contentReference[oaicite:38]{index=38}:contentReference[oaicite:39]{index=39}

## 2. Decisão  
Adotar **Redis** como:
- Cache de sessões e conversas recentes.  
- Broker de eventos via **Redis Streams**. :contentReference[oaicite:40]{index=40}:contentReference[oaicite:41]{index=41}

## 3. Consequências  
- **Positivos**: baixa latência, facilidade de configuração.  
- **Riscos**: operacional overhead, necessidade de monitorar uso de memória.  
- **Mitigação**: configurar limites de memória e alertas em Prometheus.
