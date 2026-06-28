## ADDED Requirements

### Requirement: Tokens de animação unificados
O sistema DEVE definir tokens de animação padronizados para uso em todos os frontends.

#### Scenario: Definir duração de animações
- **WHEN** frontend precisa animar um elemento
- **THEN** sistema oferece tokens de duração: `fast` (150ms), `normal` (300ms), `slow` (500ms), `cinematic` (800ms)

#### Scenario: Definir easing functions
- **WHEN** desenvolvedor configura animação
- **THEN** sistema oferece curvas predefinidas: `ease-in`, `ease-out`, `ease-in-out`, `bounce`, `elastic`

#### Scenario: Cores de animação
- **WHEN** elemento muda de estado (hover, focus, active)
- **THEN** transição de cores usa duração `fast` com easing `ease-out`

### Requirement: Timing functions padronizadas
O sistema DEVE usar funções de timing consistentes entre frontends.

#### Scenario: Entrada de elementos
- **WHEN** elemento entra na tela
- **THEN** usa `ease-out` para sensação de desaceleração natural

#### Scenario: Saída de elementos
- **WHEN** elemento sai da tela
- **THEN** usa `ease-in` para aceleração progressiva

#### Scenario: Transformações contínuas
- **WHEN** elemento muda de posição/escala continuamente
- **THEN** usa `ease-in-out` para suavidade

### Requirement: Efeitos de transição reutilizáveis
O sistema DEVE oferecer efeitos prontos para cenários comuns.

#### Scenario: Fade in/out
- **WHEN** componente é montado/desmontado
- **THEN** aplica fade com duração `normal` e opacidade 0→1 ou 1→0

#### Scenario: Slide up/down
- **WHEN** modal ou drawer abre/fecha
- **THEN** aplica slide vertical com `ease-out` e 20px de offset

#### Scenario: Zoom scale
- **WHEN** elemento é expandido ou colapsado
- **THEN** aplica scale de 0.9 para 1.0 (ou inverso) com `spring` easing

### Requirement: Motion preferences
O sistema DEVE respeitar preferências de movimento do usuário.

#### Scenario: Reduced motion
- **WHEN** usuário configura `prefers-reduced-motion`
- **THEN** sistema substitui animações complexas por fade simples

#### Scenario: No motion
- **WHEN** usuário desativa animações completamente
- **THEN** sistema remove todas as transições animadas