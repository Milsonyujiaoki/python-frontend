# Implementation Tasks - Kivy Customer App

## 1. Setup e Infraestrutura

- [ ] 1.1 Criar estrutura de diretórios do app Kivy (`frontend/kivy_customer/`)
- [ ] 1.2 Configurar `buildozer.spec` para build Android/iOS
- [ ] 1.3 Adicionar dependências: `kivy`, `kivymd`, `requests`, `Pillow`, `aiohttp`
- [ ] 1.4 Configurar SQLite local para cache offline
- [ ] 1.5 Criar sistema de rotas/navigation manager
- [ ] 1.6 Setup de variáveis de ambiente para API backend

## 2. Autenticação e Perfil (customer-profile)

- [ ] 2.1 Criar tela de login com email/senha
- [ ] 2.2 Implementar cadastro com email e telefone
- [ ] 2.3 Integração login social (Google OAuth)
- [ ] 2.4 Armazenamento seguro de JWT token
- [ ] 2.5 Tela de edição de perfil do cliente
- [ ] 2.6 Upload e crop de foto de perfil
- [ ] 2.7 Preferências de notificação (toggle)
- [ ] 2.8 Histórico de agendamentos passados
- [ ] 2.9 Lista de barbeiros favoritos
- [ ] 2.10 Exportação de dados (JSON)
- [ ] 2.11 Exclusão de conta com grace period

## 3. Agendamento de Horários (customer-appointments)

- [ ] 3.1 Tela de seleção de barbeiros com foto e rating
- [ ] 3.2 Calendário com dias disponíveis
- [ ] 3.3 Seleção de horários em slots
- [ ] 3.4 Seleção de serviços com preço e duração
- [ ] 3.5 Confirmação de agendamento com resumo
- [ ] 3.6 Validação de conflito de horário
- [ ] 3.7 Regra de antecedência mínima (30min)
- [ ] 3.8 Cancelamento de agendamento (24h regra)
- [ ] 3.9 Contador de cancelamentos por mês
- [ ] 3.10 Reagendamento rápido
- [ ] 3.11 Tela de próximos agendamentos

## 4. Sistema de Fidelidade (loyalty-program)

- [ ] 4.1 Modelo de pontos no backend
- [ ] 4.2 Creditação automática de pontos (10pts/corte)
- [ ] 4.3 Bônus de aniversário (50pts)
- [ ] 4.4 Sistema de indicação com pontos (100pts)
- [ ] 4.5 Cálculo de nível (Bronze/Silver/Gold/Platinum)
- [ ] 4.6 Tela de progresso com barra de nível
- [ ] 4.7 Badges e conquistas (UI + lógica)
- [ ] 4.8 Resgate de cupons por pontos
- [ ] 4.9 Geração de código de cupom
- [ ] 4.10 Validade e expiração de cupons
- [ ] 4.11 Histórico de resgates
- [ ] 4.12 Benefícios automáticos por nível (desconto)

## 5. Planos de Assinatura (subscription-plans)

- [ ] 5.1 CRUD de planos no backend (mensal, trimestral, semestral, anual)
- [ ] 5.2 Cálculo de desconto progressivo
- [ ] 5.3 Tela de assinatura com comparação de planos
- [ ] 5.4 Gestão de assinatura (upgrade/downgrade)
- [ ] 5.5 Cancelamento de assinatura
- [ ] 5.6 Contagem de cortes usados/disponíveis
- [ ] 5.7 Renovação automática
- [ ] 5.8 Tratamento de renovação falha (carência 7 dias)
- [ ] 5.9 Lembrete de renovação (3 dias antes)
- [ ] 5.10 Saldo visualização no dashboard

## 6. Galeria de Fotos (photo-gallery)

- [ ] 6.1 Upload de fotos pós-corte (5 fotos limite)
- [ ] 6.2 Compressão de imagens (>5MB → 2MB)
- [ ] 6.3 Organização por barbeiro (filtro)
- [ ] 6.4 Timeline cronológica
- [ ] 6.5 Controle de acesso (privacidade)
- [ ] 6.6 Cache de thumbnails offline
- [ ] 6.7 Sync em background ao reconectar
- [ ] 6.8 Compartilhamento em redes sociais
- [ ] 6.9 Watermark para não-Platinum
- [ ] 6.10 Marcar foto como privada
- [ ] 6.11 Upload em lote

## 7. Integração de Pagamentos (payment-integration)

- [ ] 7.1 Integração Asaas API (sandbox)
- [ ] 7.2 Criação de cobrança recorrente Asaas
- [ ] 7.3 Webhook Asaas (pagamento aprovado/falhou)
- [ ] 7.4 Integração Mercado Pago (checkout transparente)
- [ ] 7.5 Geração de QR Code PIX
- [ ] 7.6 Confirmação automática PIX (até 5min)
- [ ] 7.7 Salvar cartão de crédito (tokenizado)
- [ ] 7.8 Cobrança recorrente cartão
- [ ] 7.9 Atualização de cartão expirado
- [ ] 7.10 Geração de boleto (3 dias úteis)
- [ ] 7.11 Lembrete de vencimento de boleto
- [ ] 7.12 Histórico de transações completo
- [ ] 7.13 Download de recibo PDF
- [ ] 7.14 Fluxo de reembolso

## 8. Notificações Push (push-notifications)

- [ ] 8.1 Configurar Firebase Cloud Messaging (FCM)
- [ ] 8.2 Registro de device token no backend
- [ ] 8.3 Notificação de lembrete 24h antes
- [ ] 8.4 Notificação de lembrete 2h antes com ações
- [ ] 8.5 Confirmação de agendamento push
- [ ] 8.6 Promoção de aniversário
- [ ] 8.7 Campanha de reativação (30 dias inativo)
- [ ] 8.8 Respeitar opt-out de marketing
- [ ] 8.9 Notificação de novo nível alcançado
- [ ] 8.10 Notificação de badge conquistado
- [ ] 8.11 Notificação "quase lá" (10 pts faltando)
- [ ] 8.12 Renovação de assinatura confirmada
- [ ] 8.13 Pagamento pendente alerta
- [ ] 8.14 Gestão de "Não Perturbe" (horário silêncio)
- [ ] 8.15 Reset de preferências de notificação

## 9. UI/UX e Design System

- [ ] 9.1 Implementar KivyMD com tema BarberPro
- [ ] 9.2 Bottom navigation bar (padrão mobile)
- [ ] 9.3 Onboarding para primeiros usuários (3 telas)
- [ ] 9.4 Dark mode toggle
- [ ] 9.5 Splash screen com logo
- [ ] 9.6 Animações de transição between screens
- [ ] 9.7 Loading skeletons para dados
- [ ] 9.8 Error states com retry
- [ ] 9.9 Empty states ilustrados
- [ ] 9.10 Toast/snackbar para feedback
- [ ] 9.11 Dialogs de confirmação
- [ ] 9.12 Pull-to-refresh nas listas

## 10. Testes e QA

- [ ] 10.1 Testes unitários de modelos
- [ ] 10.2 Testes de integração API
- [ ] 10.3 Testes E2E de fluxo de agendamento
- [ ] 10.4 Testes de gamificação (pontos/níveis)
- [ ] 10.5 Build Android e teste em emulador
- [ ] 10.6 Build iOS e teste em simulador
- [ ] 10.7 Teste de performance (startup < 3s)
- [ ] 10.8 Teste offline (funcionalidades básicas)
- [ ] 10.9 Teste de sincronização após offline
- [ ] 10.10 Acessibilidade (fontes grandes, contraste)

## 11. Deploy e Monitoramento

- [ ] 11.1 Configurar CI/CD para builds
- [ ] 11.2 Setup de analytics (Firebase Analytics)
- [ ] 11.3 Monitoramento de crashes (Sentry)
- [ ] 11.4 Versionamento semântico de app
- [ ] 11.5 Configurar Fastlane para deploy
- [ ] 11.6 Publicação Google Play Store (内测)
- [ ] 11.7 Publicação Apple TestFlight
- [ ] 11.8 Documentação de release notes