# WeBot ChatFLOW - Documentação Técnica Frontend

## Índice
1. [Estrutura do Projeto](#estrutura-do-projeto)
2. [Módulo de Usuários](#módulo-de-usuários)
3. [Guia de Implementação de Novos Módulos](#guia-de-implementação-de-novos-módulos)

## Estrutura do Projeto
```
frontend/
├── src/
│   ├── core/
│   │   ├── domain/
│   │   │   └── entities/
│   │   ├── interfaces/
│   │   └── use-cases/
│   ├── presentation/
│   │   ├── components/
│   │   └── pages/
│   ├── infrastructure/
│   ├── shared-theme/
│   ├── config/
│   ├── assets/
│   ├── locales/
│   ├── __tests__/
│   ├── __mocks__/
│   └── types/
```

## Módulo de Usuários

### Estrutura de Arquivos
```
frontend/
├── src/
│   ├── core/
│   │   ├── domain/
│   │   │   └── entities/
│   │   │       └── User.ts
│   │   ├── interfaces/
│   │   │   └── user/
│   │   │       ├── IUserRepository.ts
│   │   │       └── IUserService.ts
│   │   └── use-cases/
│   │       └── user/
│   │           ├── CreateUser.ts
│   │           ├── UpdateUser.ts
│   │           └── DeleteUser.ts
│   ├── presentation/
│   │   ├── components/
│   │   │   └── users/
│   │   │       ├── UserForm.tsx
│   │   │       ├── UserList.tsx
│   │   │       └── UserCard.tsx
│   │   └── pages/
│   │       └── users/
│   │           ├── index.tsx
│   │           ├── create.tsx
│   │           └── edit.tsx
│   ├── infrastructure/
│   │   ├── services/
│   │   │   └── userService.ts
│   │   └── repositories/
│   │       └── userRepository.ts
│   └── types/
│       └── user.ts
```

### Exemplo de Prompt para CRUD de Usuários
```
Módulo de Usuários Frontend
O que você deseja realizar: Implementar CRUD completo de usuários no frontend

Pastas/arquivos que precisam de ajustes:

1. Tipos e Interfaces:
- src/types/user.ts
  - Definir interface User
  - Definir interface UserFormData
  - Definir tipos de resposta da API

2. Entidades e Interfaces:
- src/core/domain/entities/User.ts
  - Definir entidade User
  - Definir regras de negócio

- src/core/interfaces/user/
  - IUserRepository.ts
  - IUserService.ts

3. Use Cases:
- src/core/use-cases/user/
  - CreateUser.ts
  - UpdateUser.ts
  - DeleteUser.ts
  - GetUsers.ts

4. Infraestrutura:
- src/infrastructure/services/userService.ts
  - Implementar funções de API:
    - getUsers()
    - getUserById()
    - createUser()
    - updateUser()
    - deleteUser()

- src/infrastructure/repositories/userRepository.ts
  - Implementar interface do repositório
  - Implementar métodos de persistência

5. Componentes:
- src/presentation/components/users/UserList.tsx
  - Lista de usuários
  - Paginação
  - Filtros
  - Ações (editar, deletar)

- src/presentation/components/users/UserForm.tsx
  - Formulário de criação/edição
  - Validação de campos
  - Feedback de erros

- src/presentation/components/users/UserCard.tsx
  - Card de exibição de usuário
  - Informações básicas
  - Ações rápidas

6. Páginas:
- src/presentation/pages/users/index.tsx
  - Lista principal de usuários
  - Integração com UserList
  - Botão de criação

- src/presentation/pages/users/create.tsx
  - Página de criação
  - Integração com UserForm

- src/presentation/pages/users/edit.tsx
  - Página de edição
  - Carregamento de dados
  - Integração com UserForm

Passos para implementação:

1. Configuração Inicial:
   - Criar estrutura de pastas
   - Configurar rotas no arquivo de rotas
   - Adicionar links no menu/navegação

2. Desenvolvimento:
   - Implementar tipos e interfaces
   - Criar entidade e interfaces
   - Implementar use cases
   - Implementar serviços e repositórios
   - Desenvolver componentes
   - Implementar páginas
   - Adicionar validações
   - Implementar feedback visual

3. Testes:
   - Testar fluxo de criação
   - Testar fluxo de edição
   - Testar fluxo de deleção
   - Testar validações
   - Testar responsividade

4. Integração:
   - Conectar com backend
   - Testar integração
   - Ajustar tratamento de erros
   - Implementar loading states

5. Finalização:
   - Revisar código
   - Adicionar documentação
   - Testar em diferentes dispositivos
   - Verificar acessibilidade
```

### Exemplo de Implementação de Novo Módulo
```
Módulo de Implementação de Novos Módulos Frontend
O que você deseja realizar: Criar e integrar um novo módulo `<nome_do_módulo>` completo no frontend

Pastas/arquivos que precisam de ajustes:

1. Tipos:
- src/types/<nome_do_módulo>.ts
  - Interfaces
  - Tipos de resposta
  - Tipos de formulário

2. Entidades e Interfaces:
- src/core/domain/entities/<nome_do_módulo>.ts
  - Definir entidade
  - Definir regras de negócio

- src/core/interfaces/<nome_do_módulo>/
  - I<nome_do_módulo>Repository.ts
  - I<nome_do_módulo>Service.ts

3. Use Cases:
- src/core/use-cases/<nome_do_módulo>/
  - Create<nome_do_módulo>.ts
  - Update<nome_do_módulo>.ts
  - Delete<nome_do_módulo>.ts
  - Get<nome_do_módulo>s.ts

4. Infraestrutura:
- src/infrastructure/services/<nome_do_módulo>Service.ts
  - Funções de API
  - Tratamento de erros
  - Tipagem de respostas

- src/infrastructure/repositories/<nome_do_módulo>Repository.ts
  - Interface do repositório
  - Métodos de persistência

5. Componentes:
- src/presentation/components/<nome_do_módulo>/
  - List.tsx
  - Form.tsx
  - Card.tsx
  - Filtros.tsx

6. Páginas:
- src/presentation/pages/<nome_do_módulo>/
  - index.tsx
  - create.tsx
  - edit.tsx
  - [id].tsx

Passos para implementação:

1. Configuração:
   - Criar estrutura
   - Configurar rotas
   - Adicionar ao menu

2. Desenvolvimento:
   - Implementar tipos
   - Criar entidade e interfaces
   - Implementar use cases
   - Implementar serviços e repositórios
   - Desenvolver componentes
   - Criar páginas
   - Adicionar validações

3. Testes:
   - Testar fluxos
   - Testar validações
   - Testar responsividade

4. Integração:
   - Conectar com backend
   - Testar integração
   - Ajustar erros

5. Finalização:
   - Revisar código
   - Documentar
   - Testar dispositivos
   - Verificar acessibilidade
``` 