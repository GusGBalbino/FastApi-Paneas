# FastAPI - Paneas | Desafio

## Descrição
Este projeto é uma implementação de uma API RESTful usando FastAPI para o Desafio FastAPI da Paneas. Foca-se em práticas de desenvolvimento robustas, escalabilidade, segurança e integração com PostgreSQL e Docker.

## Requisitos do Desafio:
1. **API de Gerenciamento de Usuários:**
   - CRUD para usuários.
   - Autenticação baseada em tokens (JWT).
   - Permissões de usuário (admin, usuário regular).

2. **Integração com Banco de Dados:**
   - SQLAlchemy como ORM.
   - PostgreSQL.
   - Migrações de banco de dados com Alembic.

3. **Documentação da API:**
   - Swagger para documentação.

4. **Dockerização da Aplicação:**
   - Dockerfile para a aplicação.
   - Docker-compose para orquestração da aplicação e banco de dados.

## Pré-requisitos
- Docker
- Docker Compose

## Configuração e Execução

### Clonar o Repositório
```bash
git clone https://github.com/GusGBalbino/FastApi_Paneas.git
```

### Adicionar .env
Adicione sua .env no diretório, baseada na .env-example disponibilizada.

### Executar com Docker
A aplicação está disponível como uma imagem Docker no Docker Hub, execute os comandos a seguir:
```bash
(Linux)
docker pull balbsdev/fastapi-paneas
cd /home/{seu_user}/FastApi_Paneas
docker compose up --build
```

### Acessando a Aplicação
Após iniciar, a API estará disponível em `http://localhost:8000`.

## Documentação
A documentação Swagger está disponível em `/docs` na aplicação em execução.

## Uso da API
Utilize as rotas documentadas no Swagger para interagir com a API.

### Autenticação com JWT - No Swagger
- Registre um usuário usando a rota POST `/users/create`.
- Obtenha um 'acess_token' no response da rota POST `/users/token` utlizando as credenciais cadastradas anteriormente.
- Insira o token JWT na opção "Authentication" do Swagger para acessar as demais rotas protegidas.

### Atenção!!
- Certifique-se de deixar as portas 5432 e 8000 livres para o funcionamento do Banco de Dados e da API, respectivamente.

- Caso não seja possível liberar essas portas na sua máquina, você precisará alterar o arquivo 'docker-compose.yml' para remapear as portas do container para as portas que você deseja.
---

Desenvolvido para o Desafio FastAPI - Paneas.
