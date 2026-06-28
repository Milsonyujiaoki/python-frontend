## Why

O ecossistema BarberPro atual é funcional, mas não explora o potencial visual e de interação que as bibliotecas Python modernas (Solara, Reflex, Flet, Streamlit, Kivy) permitem. Em um mercado competitivo, **o apelo visual é o principal diferencial** — interfaces dignas de Awwwards, com animações fluidas, microinterações e estética premium, elevam a percepção de valor e engajamento do usuário.

## What Changes

- **Solara**: Implementation de Scrollytelling, cursor interativo, transições orgânicas com parallax, sliding automático de cards
- **Reflex**: Injeção de JS libraries (GSAP, Three.js, Framer Motion) via Web-Bridge para animações complexas
- **Streamlit**: Dashboards com mesh gradients, glassmorphism, gráficos flutuantes interativos
- **Flet**: Componentes mobile-first com animações nativas, gestos, e transições animadas
- **Kivy**: App do cliente com jornada gamificada, transições 3D, efeitos de partículas, bento grid interativo
- **Backend**: Arquitetura headless com idempotência (request_id), WebSockets para sync em tempo real
- **Shared Design System**: Tokens de animação, timing functions, easing curves padronizadas

## Capabilities

### New Capabilities

- `visual-design-system`: Tokens de design unificados (animações, timing, easing, transitions, effects)
- `web-bridge-integration`: Padrão para injeção de bibliotecas JS (GSAP, Three.js, Framer Motion) em frontends Python
- `websocket-realtime`: Sincronização em tempo real entre frontends via WebSockets
- `microinteractions`: Biblioteca de microinterações reutilizáveis (hover, click, focus, loading states)
- `immersive-transitions`: Transições imersivas entre telas/páginas (fade, slide, zoom, 3D transforms)

### Modified Capabilities

- `customer-appointments`: Nova UI para jornada de agendamento no Kivy com animações gamificadas
- `photo-gallery`: Interface de galeria com visualização imersiva (zoom, pan, transições)

## Impact

**Frontends afetados**: Solara, Reflex, Streamlit, Flet, Kivy

**Backend**:
- FastAPI precisa expor endpoint WebSocket para sync em tempo real
- Middleware de idempotência (request_id) para evitar duplicações
- Estrutura Clean Architecture para isolar lógica de apresentações múltiplas

**Dependencies**:
- `gsap` para animações avançadas no web
- `three.js` para elementos 3D (onde suportado)
- `py\websockets` para comunicação real-time
- Custom cursor libraries, shader support

**Arquitetura**:
- Backend headless (API-first)
- Frontends como "peles" intercambiáveis
- Web-Bridge pattern para capacidades JS nativas