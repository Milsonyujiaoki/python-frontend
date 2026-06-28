## Context

**Estado atual**: O BarberPro possui backend FastAPI funcional e 4 frontends (Solara, Reflex, Streamlit, Flet) + app Kivy em planejamento. Cada frontend usa design system básico (cores, tipografia, espaçamento) mas não explora animações avançadas, microinterações ou conceitos imersivos de UI moderna.

**Remix cultural**: Referências de estúdios premiados (Lusion, Dogstudio, Active Theory, Epic.net) combinadas com minimalismo premium (Superhuman) e gamificação mobile.

**Stack técnica**:
- Backend: FastAPI (Python 3.11+)
- Frontends web: Solara (componentes reativos), Reflex (web-bridge nativo), Streamlit (data-rich), Flet (mobile-first)
- Mobile: Kivy + KivyMD (GPU-accelerated)
- Comunicação: REST + WebSockets (em implementação)

**Stakeholders**:
- Tech Lead: Decisões de arquitetura e performance
- Designer de Interação: Especificações visuais e de movimento
- Desenvolvedores frontend: Implementação por biblioteca
- Usuários finais: Barbeiros (web dashboards), Clientes (mobile app)

## Goals / Non-Goals

**Goals:**
- Implementar animações fluidas (60fps) em todos os frontends
- Web-Bridge pattern para injeção de JS libs (GSAP, Three.js, Framer Motion)
- Cursor interativo e Scrollytelling no web
- Transições 3D e efeitos de partículas no Kivy
- Mesh gradients e glassmorphism no Streamlit
- Sincronização real-time via WebSockets
- Idempotência no backend para cliques duplos
- Tokens de animação padronizados (timing, easing, duration)

**Non-Goals:**
- Reescrever backends em outras linguagens
- Suporte a browsers legados (IE, old Safari)
- Otimização para dispositivos muito antigos (< 2018)
- Substituir bibliotecas Python por equivalentes JS
- Animações que comprometem acessibilidade (reduced motion support é opcional)

## Decisions

### 1. Web-Bridge Architecture para Animações JS

**Decisão**: Usar capacidade nativa de Reflex para injetar JavaScript via `window.eval` e `use_effect`, criando wrappers em torno de GSAP e Three.js.

**Rationale**:
- ✅ Reflex já expõe API paraEval de JS no browser
- ✅ GSAP é maduro (10+ anos), performático (300kb gzipped), ecompatível com todos browsers modernos
- ✅ Three.js para 3D tem suporte WebGL2 e é bem documentado
- ❌ Alternativa: PyScript → muito pesado (60MB+), inicialização lenta
- ❌ Alternativa: WebAssembly → complexidade desnecessária para animações DOM

**Alternativa considerada**: Componentes React via iFrame (rejeitada — isolamento quebra comunicação com Python)

**Implementação**:
```python
# Exemplo de wrapper GSAP em Reflex
import reflex as rx

class GSAPAnimator(rx.Component):
    tag = "gsap-animator"
    
    @classmethod
    def create(cls, targets: list, duration: float = 1):
        return cls(
            on_mount=window.eval(f"""
                gsap.from('{targets.join(', ')}', {{
                    duration: {duration},
                    ease: "power3.out",
                    stagger: 0.1
                }})
            """)
        )
```

### 2. Solara: Efeitos via CSS + JavaScript Injection

**Decisão**: Como Solara não tem web-bridge nativo, usar renderização HTML com CSS properties animados + injeção de JS via `solara.socketio`.

**Rationale**:
- Solara é baseado em React (via ipywidgets)
- Animações CSS (transition, animation) são GPU-accelerated
- JS injection é possível via script tags em HTML components

**Alternativa considerada**: Migrar componentes para Reflex (rejeitada — Solara tem DX superior para data-heavy apps)

### 3. Streamlit: Componentes Customizados via st.components.v1

**Decisão**: Usar Streamlit Components para injetar HTML/CSS/JS customizado com mesh gradients e glassmorphism.

**Rationale**:
- Streamlit 1.0+ suporta componentes customizados
- CSS moderno (backdrop-filter, mesh-gradient via canvas) é universal
- Performance: CSS gradients são nativos, não requerem JS runtime

**Implementação**:
```python
# mesh-gradient component
def gradient_background(colors: list[str], speed: float = 0.5):
    # Retorna componente Streamlit com canvas animado
    pass
```

### 4. Kivy: GPU-Accelerated com Canvas Instructions

**Decisão**: Usar Kivy Canvas instructions (Rectangle, Color, Rotate, Scale) com atualizações em 60fps via Clock.schedule_interval.

**Rationale**:
- Kivy renderiza via OpenGL ES 2.0+
- Partículas e transições 3D são nativos (Rotate, Scale instructions)
- Mobile performance é crítica (animações travadas = churn)

**Alternativa considerada**: Flutter (rejeitada — stack Python já estabelecida)

### 5. WebSocket First para Realtime Sync

**Decisão**: Backend expõe endpoint WebSocket (`ws://api.barberpro.app/ws`) livré via `pywebsockets` + FastAPI WebSocket route.

**Payload structure**:
```json
{
  "type": "appointment.booked",
  "payload": { "id": 123, "timestamp": "..." },
  "request_id": "uuid-v4"
}
```

**Rationale**:
- Baixa latência (< 50ms para propagate changes)
- Bidirecional (cliente não precisa poll)
- Backend centraliza estado (single source of truth)

**Alternativa considerada**: Server-Sent Events (rejeitada — apenas server→client, não serve para sync de agenda)

### 6. Idempotência via Request-ID + Dedup Window

**Decisão**: Middleware no FastAPI que extrai `X-Request-Id` header; usa Redis com TTL de 5 minutos para dedup.

**Rationale**:
- Usuários entusiasmados com UI interativa causam cliques duplos
- Idempotência previne double-booking, double-payment
- Redis é rápido (sub-millisecond), já usado no projeto

**Alternativa considerada**: Idempotência em DB (rejeitada — Redis é mais rápido para janelas curtas)

## Risks / Trade-offs

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| **Performance degradation com muitas animações** | Média | Alto | RequestAnimationFrame batching, will-change CSS, GPU layers |
| **JS injection falha em browsers restritos** | Baixa | Médio | Fallback para animações CSS puro; detectar suporte |
| **WebSocket connection drops em mobile** | Alta | Baixo | Heartbeat ping/pong, reconexão automática, fallback para polling |
| **Kivy animations travam em devices antigos** | Média | Alto | Quality settings: desativar partículas em low-end devices |
| **Complexidade de debug com animações** | Alta | Baixo | Dev mode com animation debugger, timeline visualization |
| **Three.js aumenta bundle size** | Alta | Baixo | Code splitting, load on demand, CDN hosting |
| **GSAP license (paid para commercial)** | Baixa | Médio | Usar GSAP Core (gratuito) ou Anime.js como fallback |

## Migration Plan

**Fase 1: Fundação (2 semanas)**
- [ ] Criar tokens de animação no design system shared
- [ ] Implementar middleware de idempotência no backend
- [ ] Setup WebSocket endpoint no FastAPI

**Fase 2: Web-Bridge (3 semanas)**
- [ ] Wrappers GSAP para Reflex
- [ ] Injeção JS para Solara
- [ ] Componentes custom Streamlit

**Fase 3: Kivy Imersivo (3 semanas)**
- [ ] Transições 3D entre screens
- [ ] Sistema de partículas para gamificação
- [ ] Bento grid para galeria de fotos

**Fase 4: Polimento (2 semanas)**
- [ ] Microinterações em hover/focus estados
- [ ] Cursor custom em frontends web
- [ ] Performance tuning (Lighthouse, Lighthouse CI)

**Rollback strategy**: Cada feature tem feature flag (`ENABLE_ADVANCED_ANIMATIONS`, `ENABLE_WEBSOCKETS`). Rollback = desativar flag.

## Open Questions

- GSAP comercial requer license? → Verificar termos (Core é gratuito, plugins extras são pagos)
- Kivy no iOS é suportado via buildozer? → Testar em dispositivo real
- Qual budget de performance para animações? → Definir: < 100ms perceived latency, 60fps sustained