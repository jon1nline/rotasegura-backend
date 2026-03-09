---
title: RotaSegura
emoji: 🚌
colorFrom: blue
colorTo: red
sdk: docker
pinned: false
---

# RotaSegura - Backend API

Backend Django + Django REST Framework para o aplicativo RotaSegura.

## 🚀 Configuração Inicial

### 1. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na pasta `backend` baseado em `.env.example`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8001
JWT_ACCESS_TOKEN_LIFETIME=7
JWT_REFRESH_TOKEN_LIFETIME=30
LANGUAGE_CODE=pt-br
TIME_ZONE=America/Sao_Paulo
```

### 2. Instalar Dependências

Ative o ambiente virtual e instale as dependências:

```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Aplicar Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Popular Banco de Dados

Carregue dados iniciais de exemplo:

```bash
python manage.py seed_data
```

### 5. Criar Superusuário (Opcional)

Para acessar o Django Admin:

```bash
python manage.py createsuperuser
```

### 6. Rodar o Servidor

```bash
python manage.py runserver
```

O servidor estará disponível em `http://localhost:8000`

## 📚 Documentação da API

- Swagger UI: `http://localhost:8000/docs/swagger/`

No Swagger, use **Authorize** com:

```txt
Bearer <seu_jwt_token>
```

## 📌 Endpoints Disponíveis

### Autenticação
- `POST /api/auth/register/` - Cadastro de usuário
- `POST /api/auth/login/` - Login (retorna **apenas** JWT access token)

### Incidentes
- `GET /api/incidents/` - Lista todos os incidentes
- `GET /api/incidents/?lat=-23.55&lng=-46.63&radius=3` - Filtra incidentes por raio (km), ordenados por proximidade
- `GET /api/incidents/{id}/` - Detalhes de um incidente (ID é UUID)

### Paradas de Transporte
- `GET /api/stops/` - Lista todas as paradas

### Alertas
- `GET /api/alerts/` - Lista todos os alertas

### Linhas de Transporte
- `GET /api/lines/` - Lista todas as linhas
- `GET /api/lines/?type=metro` - Filtra por tipo (metro/trem/bus)
- `GET /api/lines/{id}/itinerary/` - Itinerário de uma linha

### Reportes
- `GET /api/reports/` - Lista todos os reportes
- `POST /api/reports/` - Criar novo reporte (**requer JWT Bearer**; usuário vem do token)

### Usuário
- `GET /api/user/profile/` - Perfil do usuário (**requer JWT Bearer**)
- `PATCH /api/user/profile/update/` - Editar perfil do usuário (**requer JWT Bearer**; campos editáveis: phone, address, city, state)
- `GET /api/user/history/` - Histórico de contribuições (**requer JWT Bearer**)

## 🔐 Autenticação JWT

Este backend usa JWT com prefixo `Bearer` no header `Authorization`.

Exemplo de login:

```bash
POST /api/auth/login/
{
	"email": "usuario@email.com",
	"password": "123456"
}
```

Resposta de login:

```json
{
	"token": "<jwt_access_token>"
}
```

Exemplo de chamada autenticada:

```http
Authorization: Bearer <jwt_access_token>
```

### Endpoints Protegidos

Os seguintes endpoints **exigem autenticação JWT** e retornam dados filtrados pelo usuário autenticado (extraído do token):

- `GET /api/user/profile/` - Retorna apenas o perfil do usuário autenticado
- `GET /api/user/history/` - Retorna apenas o histórico de contribuições do usuário autenticado
- `POST /api/reports/` - Cria novo reporte associado ao usuário autenticado (ID vem do token)

Sem o token JWT válido, estes endpoints retornarão **401 Unauthorized**.

## 🆔 IDs (UUIDs)

Todos os IDs no banco de dados agora utilizam **UUID** (Universal Unique Identifier) em vez de auto-increment integers. Isso melhora a segurança e escalabilidade da API.

Exemplo de UUID:
```
GET /api/incidents/550e8400-e29b-41d4-a716-446655440000/
```

Os UUIDs são formatados como strings no padrão: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

##   Campos do Perfil do Usuário

O perfil do usuário contém os seguintes campos:

**Campos de Leitura (não editáveis):**
- `name` - Nome do usuário
- `email` - E-mail único
- `level` - Nível de contribuição (começa em 1)
- `xp` - Pontos de experiência atuais
- `maxXp` - Limite de XP para próximo nível

**Campos Editáveis:**
- `phone` - Telefone (opcional)
- `address` - Endereço completo (opcional, pode ser adicionado depois)
- `city` - Cidade (opcional, pode ser adicionado depois)
- `state` - Estado/UF (opcional, pode ser adicionado depois)

### Exemplo de Edição de Perfil

```bash
PATCH /api/user/profile/update/
Authorization: Bearer <jwt_token>

{
	"phone": "(11) 98765-4321",
	"address": "Rua das Flores, 123",
	"city": "São Paulo",
	"state": "SP"
}
```

Resposta:

```json
{
	"name": "João Silva",
	"email": "joao@email.com",
	"phone": "(11) 98765-4321",
	"address": "Rua das Flores, 123",
	"city": "São Paulo",
	"state": "SP",
	"level": 1,
	"xp": 0,
	"maxXp": 1000
}
```

##  🔧 Admin Panel

Acesse o painel administrativo em `http://localhost:8000/admin/` usando as credenciais do superusuário criado.

## 📦 Estrutura do Projeto

```
backend/
├── api/                    # Domínio principal (incidentes, alertas, reportes, linhas)
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py  # Comando para popular dados
│   ├── migrations/
│   ├── admin.py           # Configuração do admin
│   ├── authentication.py  # (Legado) classe de autenticação custom
│   ├── models.py          # Modelos de dados
│   ├── serializers.py     # Serializers DRF
│   ├── views.py           # Views/ViewSets
│   └── urls.py            # Rotas da API
├── users/                 # Domínio de usuários (auth, perfil, histórico)
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── rotasegura/            # Configurações do projeto
│   ├── settings.py        # Configurações Django
│   └── urls.py            # URLs principais
├── .venv/                 # Ambiente virtual
├── db.sqlite3             # Banco de dados SQLite
├── manage.py              # CLI do Django
└── requirements.txt       # Dependências Python
```

## 🔗 Integração com Frontend

Para conectar o frontend React Native:

1. Certifique-se de que o backend está rodando
2. No frontend, atualize `src/services/api.js` para apontar para `http://localhost:8000/api/`
3. Para testar no dispositivo físico, use o IP da máquina (ex: `http://192.168.1.X:8000/api/`)

## 🛠️ Tecnologias

- **Django 5.2** - Framework web
- **Django REST Framework 3.15** - API REST
- **SimpleJWT** - Autenticação JWT
- **drf-yasg** - Documentação Swagger/OpenAPI
- **django-cors-headers** - Habilita CORS para o frontend
- **SQLite** - Banco de dados (development)

## 📝 Próximos Passos

- [ ] Integrar com serviços de mapas externos (Google Maps API)
- [ ] Implementar WebSockets para alertas em tempo real
- [ ] Migrar para PostgreSQL em produção

## 🔧 Variáveis de Ambiente

O projeto usa arquivo `.env` para configuração de ambiente. Veja `.env.example` para uma lista completa de variáveis disponíveis.

**Variáveis principais:**

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DEBUG` | Modo debug do Django | `True` |
| `SECRET_KEY` | Chave secreta do Django | Gerado |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1` |
| `DATABASE_ENGINE` | Engine do banco de dados | `django.db.backends.sqlite3` |
| `DATABASE_NAME` | Nome do banco/arquivo | `db.sqlite3` |
| `CORS_ALLOWED_ORIGINS` | Origens CORS permitidas | `http://localhost:3000,...` |
| `JWT_ACCESS_TOKEN_LIFETIME` | Dias de validade do token | `7` |
| `JWT_REFRESH_TOKEN_LIFETIME` | Dias de validade do refresh | `30` |
| `LANGUAGE_CODE` | Código do idioma | `pt-br` |
| `TIME_ZONE` | Zona de tempo | `America/Sao_Paulo` |

**Deploy**
[Deploy Hugging Faces](https://jon1nline-rota-segura.hf.space/)

**⚠️ Importante:**
- Nunca faça commit do arquivo `.env` (está em `.gitignore`)
- A variável `DEBUG=False` deve ser usada em produção
- Gere uma nova `SECRET_KEY` para produção com: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

## 📺 Apresentação do projeto

**RotaSegura, uma PI em Desenvolvimento de Sistemas Orientado a Dispositivos Móveis e Baseados na Web**

Acesse o vídeo pelo link: https://www.youtube.com/watch?v=y41GjwnaXAI
