## Context

O projeto BarberPro possui frontends administrativos (Solara, Streamlit, Flet) mas carece de um aplicativo móvel nativo para clientes finais. Kivy foi selecionado como framework por permitir deploy multiplataforma (iOS, Android, desktop) com código Python compartilhado com o backend.

**Stakeholders:**
- Clientes da barbearia (usuários finais do app)
- Barbeiros e recepcionistas (impactados pelos agendamentos)
- Proprietários (beneficiados pela fidelização e pagamentos recorrentes)

**Referências de Design:**
- **iFood**: Jornada de agendamento simplificada
- **Nubank**: Gamificação e recompensas visuais
- **Tricorp/Tricer**: Agendamento de serviços de beleza
- **Instagram**: Galeria de fotos com navegação fluida
- **Apple Fitness+**: Progresso visual e conquistas

## Goals / Non-Goals

**Goals:**
- App mobile Kivy com jornada de agendamento em ≤3 toques
- Sistema de pontos com 4 níveis (Bronze → Platinum) e benefícios progressivos
- Planos de assinatura com cobrança recorrente via gateway
- Galeria privada de fotos com sincronização offline-first
- Notificações push para lembretes e engajamento
- Integração preparada para Asaas/Mercado Pago

**Non-Goals:**
- App para barbeiros/administração (já coberto por Solara/Streamlit)
- Rede social pública de cortes (galeria é privada)
- Processamento direto de cartão (usar gateway externo)
- Desktop/web app para clientes (foco mobile)

## Decisions

### 1. Kivy + KivyMD para UI
**Decisão:** Usar Kivy com KivyMD (Material Design) em vez de Flutter/React Native.

**Rationale:**
- Código Python compartilhado com backend
- Curva de aprendizado menor para equipe Python
- KivyMD fornece componentes Material Design prontos
- Suporte_official para iOS e Android via buildozer

**Alternativas consideradas:**
- Flutter: Requer Dart, separa frontend/backend
- React Native: Requer JavaScript/TypeScript
- Native (Swift/Kotlin): Dobro do código, mais complexo

### 2. Offline-first com SQLite local
**Decisão:** Armazenar cache local com SQLite e sincronizar quando online.

**Rationale:**
- App funciona sem conexão (cortes, agendamentos cacheados)
- Melhor UX com carregamento instantâneo
- Fotos salvas localmente antes de upload

**Alternativas consideradas:**
- Somente online: UX ruim em áreas com sinal fraco
- Full sync: Complexidade desnecessária

### 3. JWT para autenticação
**Decisão:** Usar JWT tokens com refresh automático.

**Rationale:**
- Stateless, escala melhor
- Padrão da indústria para mobile
- Backend já suporta JWT

### 4. Níveis de fidelidade fixos
**Decisão:** 4 níveis pré-definidos (Bronze: 0-99pts, Silver: 100-299, Gold: 300-599, Platinum: 600+).

**Rationale:**
- Simples de entender para usuários
- Facilita comunicação de benefícios
- Progressão clara motiva engajamento

### 5. Webhook-first para pagamentos
**Decisão:** Gateway notifica backend via webhook, app consulta status.

**Rationale:**
- Seguro (dados de pagamento não passam no app)
- Padrão do mercado
- Desacoplamento do gateway (fácil trocar Asaas ↔ Mercado Pago)

## Risks / Trade-offs

| Risco → Mitigação |
|---|
| **Build Android/iOS complexo** → Usar buildozer com perfil pré-configurado, testar em CI |
| **Performance Kivy inferior a nativo** → Otimizar imagens, lazy loading, cache agressivo |
| **Sincronização de fotos lenta** → Upload em background, compressão no cliente |
| **Webhooks falham** → Retry com backoff exponencial, endpoint de reconsulta |
| **Gamificação desbalanceada** → Começar conservador, ajustar baseado em dados |
| **App store approval** → Seguir guidelines, evitar pagamentos digitais diretos (redirecionar web) |

## Migration Plan

**Fase 1: App básico (2 semanas)**
- Setup Kivy + KivyMD
- Login/cadastro de clientes
- Listagem de barbeiros e serviços
- Agendamento simples

**Fase 2: Gamificação (1 semana)**
- Sistema de pontos
- Níveis e badges
- Tela de progresso

**Fase 3: Assinaturas (1 semana)**
- CRUD de planos
- Integração gateway (sandbox)
- Webhooks de pagamento

**Fase 4: Galeria (1 semana)**
- Upload de fotos
- Visualização por barbeiro/data
- Cache offline

**Fase 5: Notificações (3 dias)**
- Push notifications
- Lembrete de agendamento

**Rollback:** Remover change do ar, manter backend compatível.

## Open Questions

1. Qual gateway de pagamento priorizar? (Asaas tem melhor API para assinaturas)
2. Quantos pontos por corte? (sugestão: 10pts, 50pts no aniversário)
3. Benefícios de cada nível? (ex: Platinum tem 20% desconto)
4. Armazenar fotos no S3 ou local? (S3 escala melhor)
5. Limite gratuito de upload por corte? (sugestão: 5 fotos)