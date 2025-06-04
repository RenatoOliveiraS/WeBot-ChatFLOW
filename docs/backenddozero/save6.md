Abaixo segue o **save6.md** completo, gerado do zero a partir da estrutura atual em `backend/src` e `backend/src/features`. Ele resume visão geral, pré-requisitos, estrutura de pastas, configuração, principais arquivos e todas as features já implementadas.

````markdown
## 1. Visão Geral

Este backend é construído com **FastAPI** e **SQLModel**, organizado por features carregadas dinamicamente em `main.py`.  
Principais características:
- **Auth JWT** com *OAuth2PasswordBearer* e *PyJWT*  
- **Hash de senha** via PassLib/Bcrypt  
- **Relacionamentos many-to-many** (usuários ↔ departamentos/cargos)  
- **Seed automático** de usuário _admin_, departamento _“Administrador”_ e cargo _“Administrador”_  
:contentReference[oaicite:1]{index=1}

---

## 2. Pré-requisitos

- **Python 3.10+**  
- Dependências (em `requirements.txt` ou `pyproject.toml`):  
  - fastapi  
  - uvicorn  
  - sqlmodel  
  - passlib\[bcrypt]  
  - python-jwt (PyJWT)  
  - python-dotenv  
  - psycopg2-binary (opcional para PostgreSQL)  
  - python-multipart (para formulários de login)  
:contentReference[oaicite:3]{index=3}

---

## 3. Estrutura de Pastas

```plain
backend/
└── src/
    ├── __init__.py
    ├── main.py           # cria app, registra routers de features, cria tables e seed_admin_user()
    ├── config.py         # carrega .env, valida SECRET_KEY e vars ADMIN_*
    ├── db.py             # engine e get_session()
    ├── security.py       # authenticate_user, create_access_token, get_current_user
    ├── utils.py          # get_password_hash, verify_password
    └── features/
        ├── __init__.py
        ├── auth/
        │   └── router.py
        ├── users/
        │   ├── model.py
        │   ├── schemas.py
        │   ├── crud.py
        │   └── router.py
        ├── departamentos/
        │   ├── model.py
        │   ├── crud.py
        │   └── router.py
        ├── cargos/
        │   ├── model.py
        │   ├── crud.py
        │   └── router.py
        ├── email_connections/
        │   ├── model.py
        │   ├── crud.py
        │   ├── service.py
        │   └── router.py
        ├── inbound_emails/
        │   ├── model.py
        │   ├── crud.py
        │   ├── service.py
        │   └── router.py
        └── outbound_emails/
            ├── model.py
            ├── service.py
            └── router.py
````

---

## 4. Configuração

1. Na raiz `backend/`, crie o arquivo `.env` com:

   ```dotenv
   DATABASE_URL=sqlite:///./dev.db
   SECRET_KEY=<sua_chave_forte>
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ADMIN_NAME=Administrador
   ADMIN_EMAIL=admin@webot.com
   ADMIN_PASSWORD=WeBot@1234
   FERNET_KEY=<chave_base64_32_bytes>  # para criptografia de senhas em email_connections
   ```
2. Em `config.py`, use `load_dotenv()` e exponha tudo via `settings` (levanta erro se faltar SECRET\_KEY, ADMIN\_\* ou FERNET\_KEY).


---

## 5. Principais Arquivos

### main.py

* Registra automaticamente todos os `APIRouter(prefix="/<feature>")` em `features/*/router.py`.
* Executa `SQLModel.metadata.create_all(engine)` e `seed_admin_user()` (garante admin, departamento e cargo).

### config.py

* Carrega e valida variáveis de ambiente.

### db.py

* `engine = create_engine(settings.DATABASE_URL)`
* `get_session()` retorna `Session` por dependência.

### security.py

* `authenticate_user()`, `create_access_token()`, `get_current_user()` usando JWT.
* `OAuth2PasswordBearer(tokenUrl="auth/login")` (exige python-multipart).

### utils.py

* `get_password_hash()`, `verify_password()` com PassLib/Bcrypt.


---

## 6. Features

### 6.1 Auth

* **POST** `/auth/login` (form-url-encoded) recebe `username` e `password`, retorna `{ access_token }`.


### 6.2 Users

* **model.py**: `User`, `UserDepartamentoLink`, `UserCargoLink`
* **schemas.py**: `UserRead`, `DepartamentoRead`, `CargoRead`
* **crud.py**: CRUD de usuários e associações (UUID)
* **router.py**:

  * **POST** `/users/` cria usuário (Bearer admin)
  * **GET** `/users/?skip=&limit=` lista
  * **GET** `/users/{user_uuid}` detalhes
  * **GET/POST/DELETE** associações de departamentos e cargos


### 6.3 Departamentos & Cargos

Para cada:

* **model.py**, **crud.py** e **router.py**
* **GET** lista, **POST** cria e **GET** detalhe


### 6.4 Email Connections

* **model.py**: `EmailConnection` com campos básicos + timestamps.
* **crud.py**: operações CRUD.
* **service.py**: `encrypt_password()`, `decrypt_password()`, `test_email_connection()`.
* **router.py**:

  * **GET** `/email-connections/`
  * **GET/POST/PUT/DELETE** `/email-connections/{id}`
  * **POST** `/email-connections/{id}/test`
* Usa `FERNET_KEY` para criptografia em servidor.


### 6.5 Inbound Emails

* **model.py**: `InboundEmail` (headers, corpo, anexos, JSON em colunas).
* **crud.py**: `create_inbound_email()`, `get_inbound_emails()`, `get_inbound_email()`.
* **service.py**:

  * `ingest_raw_email()` (parse RFC-822/MIME)
  * `fetch_inbound_emails()` (IMAP UNSEEN)
* **router.py**:

  * **POST** `/inbound-emails/webhook`
  * **POST** `/email-connections/{id}/fetch`
  * **GET** `/inbound-emails` e `/inbound-emails/{email_id}`


### 6.6 Outbound Emails

* **model.py**: `SendEmailPayload`, `ReplyEmailPayload`.
* **service.py**: `send_email()`: busca conexão SMTP, descriptografa senha, monta mensagem (headers/IDs), envia via `smtplib`.
* **router.py**:

  * **POST** `/outbound-emails/send`
  * **POST** `/outbound-emails/{inbound_email_id}/reply`
* Cuidados: timeouts, exceções, testes com `smtpd.DebuggingServer`.


---

## 7. Como adicionar nova **feature**

1. Crie pasta `src/features/<nome>/` com `__init__.py`.
2. Dentro, crie:

   * `model.py` com `class X(SQLModel, table=True)` (+ relações)
   * `crud.py` com lógica de DB
   * `router.py` com `APIRouter(prefix="/<nome>")`
3. Reinicie Uvicorn: a rota será registrada automaticamente.


---

## 8. Execução

```bash
cd backend
uvicorn src.main:app --reload
```

* **Swagger UI**: `http://127.0.0.1:8000/docs`
* **OpenAPI JSON**: `http://127.0.0.1:8000/openapi.json`

```

Qualquer ajuste ou feature nova, basta seguir o padrão acima e atualizar este save6.
```


````markdown
# Documentação: Identificador Personalizado (WB<ID>) para Inbound/Outbound

## 1. Objetivo
Registrar a ideia de introduzir um identificador personalizado (WB\<ID\>) no fluxo de envio e resposta de e-mails (inbound/outbound), de forma a:
- Facilitar o rastreamento e associação de mensagens;
- Manter a base de dados mais “limpa”, armazenando apenas o conteúdo relevante (fluxo de conversa entre marcadores);
- Permitir flexibilidade futura para ajustes na lógica de associação.

> **Nota crítica**:  
> - O termo “UUID” foi usado inicialmente, mas a proposta final é um identificador customizado com prefixo estático (`WB`) seguido de um bloco numérico/alfanumérico.  
> - É importante analisar colisões de IDs e definir claramente o formato para evitar duplicidades.  

---

## 2. Contexto Atual
Atualmente, o sistema de inbound/outbound possui:
1. **reply_to_id** (geralmente uma string ou número retornado pelo servidor SMTP) que identifica a que mensagem estamos respondendo.  
2. Fluxo de processamento (no backend em FastAPI/SQLModel) em que:
   - Quando chega um e-mail inbound, ele é parseado, salvo em tabela `inbound_emails` com seus metadados (assunto, remetente, corpo, anexos, headers etc).  
   - Ao enviar (outbound) uma resposta, usa-se `inbound_email_id` ou `reply_to_id` para preencher os headers corretos (Thread-Index, In-Reply-To, References).  
   - Internamente, há relacionamentos entre as tabelas (por exemplo, `InboundEmail` ↔ `OutboundEmail`) com base nesse `reply_to_id` ou `message_id`.  

### Limitação Atual
- O `reply_to_id` pode ser curto ou genérico (geralmente fornecido pelo servidor de e-mail), dificultando:
  - **Consulta direta**: ao buscar logs ou threads, precisamos “converter” aquele ID em registros correlacionados.  
  - **Armazenamento de histórico**: manter todo o corpo (headers + conteúdo) resulta em registros grandes e pouco “estruturados” para análise de conversa.  

---

## 3. Proposta de Identificador Personalizado
Criar um campo adicional (ex.: `wb_id` ou `wb_uuid`) com formato fixo e prefixo estático `WB`, que:
1. **Prefixo “WB”**: indica que foi gerado pelo nosso sistema (WebotBot ou similar).  
2. **Sequência numérica/alfanumérica**:  
   - Pode ser apenas incremental (`WB00000001`, `WB00000002` …), ou  
   - Combinar timestamp + sequência aleatória (ex.: `WB20250602A3F4B7C8`), ou  
   - Gerar um UUID v4 e converter para um formato legível (ex.: `WB-6f1e7a9c-...`).  

### Vantagens
- **Rastreabilidade**: ao incluir `WB<ID>` no corpo da mensagem de retorno, fica trivial localizar no banco de dados qual “conjunto” de texto antecede e sucede aquele marcador.  
- **Performance de consulta**: em vez de buscar em colunas de texto livre, basta filtrar por `wb_id` para recuperar todas as “pontas” (início e fim da conversa).  
- **Limpeza de dados**: armazenar somente o conteúdo que ocorre _entre_ os marcadores, evitando salvar repetições de cabeçalhos ou trechos já processados.  

### Desvantagens / Pontos de Atenção
1. **Riscos de Colisão**  
   - Se usarmos apenas sequência numérica, devemos garantir atomicidade ao gerar e persistir o próximo `WB<ID>`.  
   - Caso optemos por UUID puro (sem prefixo manual), a colisão é praticamente nula, mas o identificador fica “grande” (36 caracteres).  
2. **Formatação no Corpo de E-mail**  
   - Clientes de e-mail podem interpretar caracteres de forma diferente; é recomendável usar delimitadores fixos e únicos (por exemplo, sempre `UUID: WBxxxxx` em linha própria).  
   - É preciso padronizar quebra de linha antes e depois dos marcadores para evitar “misturar” texto com o conteúdo relevante.  
3. **Manutenção de Versões**  
   - Se no futuro mudarmos o prefixo ou o formato, teremos dois tipos de identificadores no histórico.  
   - Talvez seja útil gravar no banco de dados um campo extra que indique a “versão do marcador” (por exemplo, `wb_scheme_version = 1`), para distinguir formatos futuros.  

---

## 4. Exemplo de Fluxo de Mensagem

### 4.1 Inbound (Recebimento)
1. Chega um e-mail novo, é parseado e gravado na tabela `inbound_emails`.  
2. Gera-se o `wb_id` (por exemplo, `WB00000123`) no momento do recebimento.  
3. No campo `body_raw` (ou equivalente), armazena-se **apenas** o conteúdo entre marcadores (definido pelo remetente ou sistema anterior).  
   - **Opcional**: O sistema pode inserir temporariamente marcadores provisórios para delimitar, para posterior edição manual automática.  

### 4.2 Outbound (Resposta)
Ao retornar resposta ao e-mail original:
```text
-------------responder esse e-mail acima dessa mensagem ------------------
UUID: WB00000123

INFORMAÇÕES DO EMAIL
(UUID: WB00000123)

-------------responder esse e-mail abaixo dessa mensagem ------------------
````

1. O backend recupera o `inbound_email` correspondente a `WB00000123`.
2. Monta o corpo de resposta do “meio” (conteúdo que efetivamente interessa), sem duplicar cabeçalhos.
3. Adiciona os marcadores exatamente como especificado, garantindo que:

   * A parte “acima” contenha instruções padronizadas (para quem for digitar a resposta).
   * A parte “INFORMAÇÕES DO EMAIL” contenha metadados que possam ser úteis (por exemplo, remetente, data, assunto).
   * A parte “abaixo” fique vazia para o usuário digitar ou para inserir um template específico.

### 4.3 Armazenamento no Banco

* Na tabela `inbound_emails`:

  * `wb_id`: `WB00000123`
  * `content`: deve conter apenas o texto “entre os delimitadores”, ou seja, o que interessa processar.
* Na tabela `outbound_emails`:

  * `inbound_wb_id`: referência para `WB00000123` (FK ou coluna simples).
  * `wb_id`: pode ser opcional, caso queiramos rastrear respostas de respostas (threads aninhadas).
  * `content`: texto “entre os delimitadores” inserido pelo usuário ou template.

---

## 5. Estrutura Sugerida para o Documento de Requisitos

````markdown
# Documento de Requisitos — Identificador Personalizado WB<ID>

## 1. Introdução
Breve descrição do propósito do documento e contexto geral (inbound/outbound).

## 2. Definições
- **WB<ID>**: identificador personalizado para mensagens.
- **Delimitador Acima**: marcador que delimita início do trecho de resposta.
- **Delimitador Abaixo**: marcador que delimita fim do trecho de resposta.

## 3. Formato do Identificador
- Prefixo fixo: `WB`
- Parte numérica ou alfanumérica:  
  - Exemplo sequence-based: `WB00000001`  
  - Exemplo timestamp+aleatório: `WB20250602A3F4B7C8`  
- **Regra de geração**:  
  - Deve ser único globalmente.
  - Deve ser indexado no banco de dados para busca rápida.
  - (Opcional) Versão do esquema: `wb_scheme_version = 1`.

## 4. Exemplo de Corpo de E-mail com Marcadores
```text
-------------responder esse e-mail acima dessa mensagem ------------------
UUID: WB00000123

INFORMAÇÕES DO EMAIL
UUID: WB00000123

-------------responder esse e-mail abaixo dessa mensagem ------------------
````

* Linha 1: marcador inicial para contextualizar instruções.
* Linha 2: `UUID: WB<ID>` idêntico ao do registro inbound.
* Linhas 4–6: seção “INFORMAÇÕES DO EMAIL”, pode conter cabeçalhos resumidos.
* Duplicar `UUID: WB<ID>` dentro das informações para reforçar a correlação.
* Linha final: marcador para início da resposta efetiva.

## 5. Fluxo de Processamento

1. **Recebimento (Inbound)**
   a. Ingestão no serviço IMAP/Webhook.
   b. Geração de `WB<ID>` (função `generate_wb_id()`).
   c. Salvamento em `inbound_emails`:

   ```sql
   INSERT INTO inbound_emails (wb_id, subject, sender, body_raw, created_at) VALUES ('WB00000123', 'Assunto X', 'remetente@ex.com', '...texto entre marcadores...', NOW());
   ```

   d. Opcional: encaminhar para workflow de processamento.

2. **Resposta (Outbound)**
   a. Usuário/serviço solicita “responder `WB00000123`”.
   b. Backend busca `inbound_emails` pelo `wb_id`.
   c. Monta modelo de corpo conforme seções padronizadas.
   d. Usuário insere resposta no local correto.
   e. Ao salvar, registra em `outbound_emails`:

   ```sql
   INSERT INTO outbound_emails (inbound_wb_id, wb_id, body_raw, created_at) VALUES ('WB00000123', 'WB00000456', '...texto digitado...', NOW());
   ```

   f. Envia e-mail via SMTP, preenchendo `In-Reply-To` e `References` com `reply_to_id` original + cabeçalhos do servidor.

## 6. Geração de WB<ID> (Sugestões)

* **Opção 1: Sequence-Based**

  * Tabela auxiliar `wb_sequence` com campo `last_id INT`.
  * Ao gerar:

    1. `UPDATE wb_sequence SET last_id = last_id + 1;`
    2. `SELECT last_id FROM wb_sequence;`
    3. Formatar `WB` + zero-padding (ex.: 10 dígitos).
* **Opção 2: UUID v4 (Reduz colisão)**

  * Gera-se `uuid.uuid4()` no backend.
  * Converte para string (36 caracteres), remove hífens ou mantém, ex.: `WB-6f1e7a9c-...`.
  * Vantagem: praticamente zero probabilidade de colisão.
  * Desvantagem: maior uso de armazenamento + Índice maior.
* **Opção 3: Timestamp + Aleatório**

  * `WB` + `YYYYMMDDHHMMSS` + 4 caracteres hex aleatórios.
  * Ex.: `WB20250602091532A3F4`.
  * Colisão: extremamente baixa dentro de intervalos curtos, mas requer atomicidade caso múltiplas requisições ao mesmo segundo.

## 7. Tabelas e Campos Recomendados

### 7.1 inbound\_emails

| Campo          | Tipo        | Observações                                                                    |
| -------------- | ----------- | ------------------------------------------------------------------------------ |
| id             | UUID/serial | Chave primária tradicional (p. ex. UUID v4 ou serial).                         |
| wb\_id         | VARCHAR(32) | Identificador customizado (ex.: `WB00000123`). Deve ter índice único.          |
| message\_id    | VARCHAR     | Cabeçalho `Message-ID` original do e-mail.                                     |
| reply\_to\_id  | VARCHAR     | Cabeçalho `In-Reply-To`, caso exista.                                          |
| subject        | VARCHAR     | Assunto do e-mail.                                                             |
| sender         | VARCHAR     | Remetente.                                                                     |
| recipients     | JSON/ARRAY  | Lista de destinatários.                                                        |
| body\_clean    | TEXT        | Texto extraído **entre** os marcadores (sem cabeçalhos duplicados).            |
| metadata\_json | JSON        | Cabeçalhos completos ou metadados adicionais (data, size, attachments, flags). |
| created\_at    | TIMESTAMP   | Data/hora de recebimento.                                                      |

### 7.2 outbound\_emails

| Campo           | Tipo        | Observações                                                                                              |
| --------------- | ----------- | -------------------------------------------------------------------------------------------------------- |
| id              | UUID/serial | Chave primária.                                                                                          |
| inbound\_wb\_id | VARCHAR(32) | FK para `inbound_emails.wb_id`. Índice secundário para buscas por threads.                               |
| wb\_id          | VARCHAR(32) | Opcional: caso a resposta gere uma nova sub-thread.                                                      |
| message\_id     | VARCHAR     | `Message-ID` do e-mail enviado.                                                                          |
| in\_reply\_to   | VARCHAR     | Cabeçalho `In-Reply-To` (igual ao `message_id` original do inbound, ou `WB...` se quisermos customizar). |
| subject         | VARCHAR     | Assunto.                                                                                                 |
| recipients      | JSON/ARRAY  | Destinatários.                                                                                           |
| body\_clean     | TEXT        | Texto efectivamente enviado (entre marcadores).                                                          |
| metadata\_json  | JSON        | Outros cabeçalhos e dados (data de envio, status de entrega, bounces, etc.).                             |
| created\_at     | TIMESTAMP   | Data/hora de envio.                                                                                      |

## 8. Exemplo de Função para Geração de `WB<ID>` (Pseudo-código Python)

```python
import uuid
import datetime

def generate_wb_id(sequence_based: bool = False) -> str:
    if sequence_based:
        # Exemplo usando tabela de sequência no banco
        # (executar UPDATE e SELECT em transação atômica)
        next_id_int = get_next_sequence_from_db('wb_sequence')
        return f"WB{str(next_id_int).zfill(10)}"
    else:
        # Exemplo usando UUID v4 reduzido
        raw_uuid = uuid.uuid4()
        # Opcional: remover hífens e pegar primeiros 12 caracteres
        short_uuid = raw_uuid.hex[:12].upper()
        return f"WB{short_uuid}"
```

> **Critério crítico**:
>
> * Caso opte por `short_uuid`, garantir que os 12 primeiros caracteres sejam suficientes para evitar colisões em escala de volume esperado.
> * Se o uso for intensivo (milhares de e-mails por segundo), considerar `timestamp + random` ou sequence-based para performance.

---

## 9. Possíveis Ajustes Futuros

1. **Versão do Marcador**

   * Se mudarmos o padrão (ex.: prefixo “WB2” ou formato alfanumérico diferente), manter uma coluna extra `wb_scheme_version` para diferenciar.
2. **Sincronização com Outros Sistemas**

   * Caso haja integração com CRM, chatbots ou plataformas externas, padronizar o mapeamento `WB<ID>` ↔ `external_thread_id`.
3. **Armazenamento de Histórico Completo**

   * Se for necessário arquivar raias completas de conversa (headers + corpo), podemos criar tabela `email_history` que recolha versões antigas, mantendo o `wb_id` como chave para reconstrução.
4. **Interface de Consulta**

   * Desenvolver endpoint `/threads/{wb_id}` que retorne todo o histórico de inbound/outbound linked pelo mesmo `wb_id`.
   * Possibilitar filtros por data, remetente, status de envio etc.
5. **Validação de Texto no Cliente**

   * Se os usuários editam manualmente o template (em web UI ou cliente de e-mail), implementar validação para que não quebrem os marcadores (por exemplo, impedindo remoção/alteração de “UUID: WB…”).

---

## 10. Conclusão

* A ideia central de introduzir um identificador personalizado `WB<ID>` tem mérito para melhorar rastreabilidade e organização dos fluxos de e-mail.
* É fundamental escolher e documentar bem o formato (colisões, performance, versionamento).
* O documento acima registra a proposta inicial e serve como base para implementação e ajustes futuros.

> **Próximos passos sugeridos**:
>
> 1. Definir qual estratégia de geração (sequence-based, UUID curto ou timestamp+aleatório) melhor atende ao volume e pereça.
> 2. Criar migration/alteração nas tabelas `inbound_emails` e `outbound_emails` para adicionar `wb_id`.
> 3. Ajustar serviços de ingestão (em `service.py`) e rotas de envio/response (`router.py`) para manipular `wb_id`.
> 4. Elaborar testes automatizados que validem:
>
>    * Geração única de `wb_id`.
>    * Montagem correta dos blocos de mensagem com marcadores.
>    * Resgate consistente dos dados “entre marcadores” para cada `wb_id`.
> 5. Revisar periodicamente (checkpoint em 3 meses) a performance e possíveis colisões de IDs.

```

**Observações finais**:  
- Busquei ser crítico sobre colisões e versionamento, evitando aprisionar a solução a um único formato (UUID puro ou sequência fixa).  
- A ideia de “manter apenas o conteúdo nas extremidades” traz clareza, mas lembre-se de armazenar metadados essenciais (remetente, assunto, data) num campo separado (`metadata_json`).  
- Em vez de chamar “UUID”, denomine de “WB_ID” (ou similar) para não confundir com UUID padrão.
```
