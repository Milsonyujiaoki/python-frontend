## ADDED Requirements

### Requirement: Conexão WebSocket bidirecional
O sistema DEVE estabelecer conexão WebSocket para comunicação em tempo real.

#### Scenario: Estabelecer conexão
- **WHEN** cliente carrega aplicação
- **THEN** sistema abre WebSocket para `ws://api.barberpro.app/ws`

#### Scenario: Autenticação via WebSocket
- **WHEN** cliente conecta
- **THEN** sistema envia JWT token no handshake (`ws://...?token=eyJ...`)

#### Scenario: Reconexão autômatica
- **WHEN** conexão cai (network issue)
- **THEN** sistema tenta reconectar com exponential backoff (1s, 2s, 4s, 8s, máx 30s)

### Requirement: Eventos de agenda em tempo real
O sistema DEVE sincronizar mudanças de agenda instantaneamente entre frontends.

#### Scenario: Agendamento bookado
- **WHEN** cliente booka horário via Kivy
- **THEN** sistema notifica todos os barbeiros conectados via `appointment.booked`

#### Scenario: Agendamento cancelado
- **WHEN** cliente cancela agendamento
- **THEN** sistema envia `appointment.cancelled` e atualiza UI dos barbeiros em < 500ms

#### Scenario: Conflito de horário
- **WHEN** dois clientes tentam bookar mesmo horário
- **THEN** sistema aceita primeiro (via request_id) e rejeita segundo com `409 Conflict`

### Requirement: Mensagens com idempotência
O sistema DEVE suportar request_id para mensagens idempotentes.

#### Scenario: Envio com request_id
- **WHEN** cliente envia mensagem `appointment.book`
- **THEN** inclui `request_id: uuid-v4` no payload

#### Scenario: Dedup no backend
- **WHEN** backend recebe request_id duplicado (dentro de 5min)
- **THEN** retorna resposta cacheada sem reprocessar

#### Scenario: Response com request_id
- **WHEN** backend responde
- **THEN** inclui mesmo `request_id` da requisição para correlação

### Requirement: Heartbeat e health check
O sistema DEVE manter conexão viva e detectar dead peers.

#### Scenario: Ping/Pong heartbeat
- **WHEN** conexão estáEstablished
- **THEN** cliente envia ping a cada 30 segundos; servidor responde pong

#### Scenario: Detecção de conexão morta
- **WHEN** servidor não recebe ping por 90 segundos
- **THEN** sistema fecha conexão e notifica outros clients

#### Scenario: Health check endpoint
- **WHEN** cliente quer verificar status
- **THEN** pode enviar `{"type": "ping"}` e recebe `{"type": "pong", "server_time": "..."}`

### Requirement: Grupamento por rooms
O sistema DEVE suportar rooms para broadcast seletivo.

#### Scenario: Join room de barbearia
- **WHEN** barbeiro faz login
- **THEN** sistema join na room `barbershop:{id}`

#### Scenario: Broadcast para barbeiros
- **WHEN** cliente booka horário
- **THEN** sistema broadcast apenas para room `barbershop:{id}` (não todos os usuários)

#### Scenario: Leave room
- **WHEN** usuário desconecta
- **THEN** sistema remove automaticamente de todas as rooms