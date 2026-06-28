## ADDED Requirements

### Requirement: Transições entre telas/páginas
O sistema DEVE animar transições de navegação de forma fluida.

#### Scenario: Fade transitions
- **WHEN** usuário navega entre páginas
- **THEN** sistema aplica fade out (200ms) → swap → fade in (300ms)

#### Scenario: Slide transitions
- **WHEN** navegação é forward/backward
- **THEN** sistema aplica slide horizontal (direita para forward, esquerda para back)

#### Scenario: Zoom transitions
- **WHEN** usuário abre detalhe de item
- **THEN** sistema aplica zoom in a partir do elemento clicado (shared element transition)

### Requirement: Transições 3D
O sistema DEVE suportar transformações 3D para imersão.

#### Scenario: Flip card
- **WHEN** usuário clica em card virável
- **THEN** sistema aplica rotateY 180deg com perspective e preserve-3d

#### Scenario: Cube transition
- **WHEN** usuário navega em carousel 3D
- **THEN** sistema aplica rotação cúbica com transform-style: preserve-3d

#### Scenario: Parallax scrolling
- **WHEN** usuário faz scroll
- **THEN** elementos de fundo movem mais lentamente que foreground (30-50% speed)

### Requirement: Scrollytelling
O sistema DEVE(trigger) animações baseadas em scroll position.

#### Scenario: Animate on scroll enter
- **WHEN** elemento entra na viewport
- **THEN** sistema trigger animação de entrada (fade + slide up)

#### Scenario: Scroll-triggered progress
- **WHEN** usuário scrolla através de seção
- **THEN** barra de progresso preenche proporcionalmente ao scroll

#### Scenario: Sticky sections
- **WHEN** usuário scrolla em seção sticky
- **THEN** próximo slide sobrepõe anterior com crossfade

### Requirement: Carrossel com sliding automático
O sistema DEVE oferecer carrossel com auto-play e transições fluidas.

#### Scenario: Auto-play
- **WHEN** carrossel está visível
- **THEN** sistema avança slide a cada 5 segundos com crossfade ou slide

#### Scenario: Pause on hover
- **WHEN** cursor passa sobre carrossel
- **THEN** sistema pausa auto-play

#### Scenario: Distorção sutil no slide
- **WHEN** slide está transitando
- **THEN** sistema aplica leve skew ou wave distortion (GSAP custom)

### Requirement: Transições mobile (Kivy)
O sistema DEVE animações otimizadas para jornada mobile.

#### Scenario: Screen swipe
- **WHEN** usuário swipe horizontal no mobile
- **THEN** sistema transição de screen com slide跟随 finger

#### Scenario: 3D cube navigation
- **WHEN** usuário navega entre seções do app
- **THEN** sistema aplica rotação de cubo 3D (90deg por face)

#### Scenario:_shared element transition
- **WHEN** usuário clica em foto da galeria
- **THEN** foto expande para full-screen a partir da posição original

### Requirement: Modal e overlay transitions
O sistema DEVE animar entrada/saída de modais e overlays.

#### Scenario: Modal fade-scale
- **WHEN** modal abre
- **THEN** sistema aplica fade + scale de 0.9 para 1.0 em 300ms

#### Scenario: Backdrop blur
- **WHEN** modal está aberto
- **THEN** sistema aplica blur no background (backdrop-filter: blur(4px))

#### Scenario: Drawer slide
- **WHEN** drawer lateral abre
- **THEN** sistema aplica slide horizontal da borda com shadow progressivo