## Why

Clientes de barbearias precisam de uma experiência mobile nativa para agendar horários, acompanhar seus cortes e ser recompensados por sua fidelidade. Atualmente, o sistema possui apenas frontends administrativos (Solara, Streamlit, Flet). Este change cria um **app mobile dedicado para clientes** usando Kivy, transformando a experiência do usuário final com gamificação, planos de assinatura e galeria privada de histórico de cortes.

## What Changes

- **Novo app mobile Kivy** para clientes finais (iOS/Android via Kivy)
- **Sistema de agendamento** de horários com barbeiros específicos
- **Galeria privada de fotos** dos cortes realizados por barbeiro/data
- **Sistema de gamificação** com pontos, níveis e cupons progressivos
- **Planos de assinatura** (mensal, trimestral, semestral, anual) de cortes
- **Preparação para gateway de pagamento** (Asaas, Mercado Pago)
- **Jornada do usuário** otimizada para self-service mobile

## Capabilities

### New Capabilities

- `customer-appointments`: Agendamento de horários com seleção de barbeiro, serviço e unidade
- `loyalty-program`: Sistema de pontos, níveis (Bronze, Silver, Gold, Platinum) e resgate de cupons
- `subscription-plans`: Planos recorrentes de cortes (mensal, trimestral, semestral, anual)
- `photo-gallery`: Galeria privada de fotos dos cortes históricos por cliente
- `payment-integration`: Interface para gateways de pagamento (Asaas, Mercado Pago)
- `customer-profile`: Perfil do cliente com preferências, histórico e conquistas
- `push-notifications`: Notificações push para lembretes de agendamento, promoções e conquistas

### Modified Capabilities

- `kivy-frontend`: Expande de frontend genérico para app mobile completo focado em jornada do cliente

## Impact

**Novas Dependências:**
- `kivy` (já existente, expandido)
- `kivymd` para Material Design no mobile
- `requests` para comunicação com API
- `Pillow` para manipulação de imagens
- `sqlite3` para cache local offline-first

**API Backend:**
- Novos endpoints para agendamentos, gamificação, assinaturas e upload de fotos
- Autenticação JWT para clientes móveis
- Webhooks para confirmação de pagamentos

**Sistemas Externos (futuro):**
- Asaas API (pagamentos recorrentes, PIX)
- Mercado Pago API (checkout transparente, PIX)
- Firebase Cloud Messaging / APNs (notificações push)

**UX/UI:**
- Design mobile-first com referências: iFood (jornada), Nubank (gamificação), Tricorp (agendamento)
- Navegação por tabs inferior (padrão mobile)
- Onboarding para primeiros usuários
- Dark mode suportado