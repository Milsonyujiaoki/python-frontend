# ✂️ BarberPro - Frontend Systems Documentation

## 🎯 Visão Geral

Sistema de gestão para barbearias com **4 frontends distintos**, cada um com identidade visual única baseada em referências de mercado, compartilhando o mesmo backend API.

---

## 🖥️ Frontends Disponíveis

### 1. Solara (Port 8080) - **Recomendado para Desenvolvimento**
**Design Reference:** Linear + Vercel

- **URL:** http://localhost:8080
- **Estilo:** Clean, developer-focused, minimalista
- **Cores:** Violet/Purple (#7c3aed)
- **Features:**
  - Sidebar navigation fixa
  - Cards com gradientes modernos
  - Integração completa com API
  - Loading states e error handling
  - Responsive layout

**Arquivo:** `frontend/solara/main.py`

---

### 2. Streamlit (Port 8082) - **Dashboard Profissional**
**Design Reference:** Stripe Dashboard + Shopify

- **URL:** http://localhost:8082
- **Estilo:** Data-rich, profissional, analytics-focused
- **Cores:** Stripe purple (#635bff) + Emerald green
- **Features:**
  - Métricas estilo Stripe (gradient cards)
  - Tabelas de dados interativas
  - Filtros e busca avançada
  - Forms de cadastro integrados
  - Charts e gráficos

**Arquivo:** `frontend/streamlit_updated/main.py`

---

### 3. Flet (Port 8083) - **Mobile-First PWA**
**Design Reference:** Instagram + Twitter Mobile

- **URL:** http://localhost:8083 (requer `pip install flet`)
- **Estilo:** Social media app, touch-friendly
- **Cores:** Instagram gradient (purple → orange)
- **Features:**
  - Bottom navigation bar
  - Stories-style quick actions
  - Card-based feed layout
  - Avatar circles com gradientes
  - Mobile-optimized UX

**Arquivo:** `frontend/flet/main.py`

---

### 4. Backend API (Port 8000)
**Design Reference:** FastAPI padrão + CORS configurado

- **URL:** http://localhost:8000
- **Docs:** http://localhost:8000/api/v1/docs
- **Features:**
  - CORS habilitado para todos os frontends
  - Error handling global
  - Response timing headers
  - Health check endpoint
  - Branding customization via settings

**Arquivo:** `backend/app/main.py`

---

## 🎨 Design System Compartilhado

Localizado em `frontend/shared/design/theme.py`:

```python
# Design Tokens
- ColorPalette (50-900 scales)
- Typography (Inter font family)
- Spacing (8px base scale)
- BorderRadius (4px - 24px)
- Shadow (xs - 2xl elevations)

# Temas
- get_light_theme()
- get_dark_theme()

# CSS Generator
- generate_css_variables(theme)
- export_theme_json()
```

---

## 🚀 Como Rodar

### Backend (sempre primeiro)
```bash
cd backend
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Solara
```bash
solara run frontend/solara/main.py --port 8080
```

### Streamlit
```bash
streamlit run frontend/streamlit_updated/main.py --server.port 8082
```

### Flet
```bash
pip install flet
python3 -m flet run frontend/flet/main.py --port 8083
```

---

## 📊 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/customers/` | Listar clientes |
| POST | `/api/v1/customers/` | Criar cliente |
| GET | `/api/v1/barbers/` | Listar barbeiros |
| POST | `/api/v1/barbers/` | Criar barbeiro |
| GET | `/api/v1/services/` | Listar serviços |
| POST | `/api/v1/services/` | Criar serviço |
| GET | `/health` | Health check |
| GET | `/api/v1/docs` | Swagger UI |

---

## 🎯 Identidade Visual por Frontend

### Solara (Linear/Vercel)
- **Foco:** Desenvolvedores, SaaS moderno
- **Cor:** Violet (#7c3aed)
- **Tipografia:** Inter
- **Sombras:** Subtle, elevation-based
- **Animações:** 200-300ms ease

### Streamlit (Stripe/Shopify)
- **Foco:** Business owners, analytics
- **Cor:** Stripe purple (#635bff)
- **Tipografia:** Inter + System fonts
- **Gradientes:** Multi-color metrics
- **Layout:** Dense information display

### Flet (Instagram/Twitter)
- **Foco:** Mobile users, quick actions
- **Cor:** Instagram gradient
- **Tipografia:** System fonts
- **Navegação:** Bottom tab bar
- **Componentes:** Stories, cards, feeds

---

## 📁 Estrutura de Arquivos

```
frontend/
├── shared/
│   └── design/
│       ├── theme.py          # Design system core
│       └── __init__.py
├── solara/
│   └── main.py               # Linear/Vercel style
├── streamlit_updated/
│   └── main.py               # Stripe/Shopify style
└── flet/
    └── main.py               # Instagram/Twitter style

backend/
└── app/
    ├── main.py               # FastAPI com CORS + error handling
    ├── core/
    │   └── config.py         # Settings + branding
    ├── api/v1/
    │   ├── customers.py
    │   ├── barbers.py
    │   └── services.py
    ├── crud.py               # Database operations
    ├── models.py             # SQLAlchemy models
    └── schemas.py            # Pydantic schemas
```

---

## 🔧 Configurações de Branding

No backend (`backend/app/core/config.py`):

```python
BRAND_NAME: str = "BarberPro"
BRAND_COLOR_PRIMARY: str = "#6366f1"
BRAND_COLOR_SECONDARY: str = "#10b981"
BRAND_FONT: str = "Inter, system-ui, sans-serif"
```

---

## ✅ Status dos Servidores

| Serviço | Porta | Status | URL |
|---------|-------|--------|-----|
| Backend API | 8000 | ✅ | http://localhost:8000 |
| Solara | 8080 | ✅ | http://localhost:8080 |
| Streamlit | 8082 | ✅ | http://localhost:8082 |
| Flet | 8083 | ⚠️ | Requer `pip install flet` |

---

## 🎨 Referências de Design

1. **Linear** (linear.app) - Clean, minimal, developer tools
2. **Vercel** (vercel.com) - Bold typography, gradients
3. **Stripe** (stripe.com) - Professional fintech UI
4. **Shopify** (shopify.com) - E-commerce dashboard
5. **Instagram** - Social media engagement patterns
6. **Twitter** - Feed-based content display
7. **Nubank** - Fintech brasileiro, cores vibrantes
8. **Apple** - Premium, polished interfaces
9. **Toyota** - Clean, functional design

---

## 📝 Próximos Passos

1. **Autenticação Real** - Implementar JWT auth
2. **Appointment Management** - CRUD completo de agendamentos
3. **Dark Mode** - Toggle entre temas claro/escuro
4. **Custom Branding** - Upload de logo e cores personalizadas
5. **Real-time Updates** - WebSocket para atualizações em tempo real
6. **Push Notifications** - Lembretes de agendamento

---

**Versão:** 1.0.0  
**Última Atualização:** 2026-06-27