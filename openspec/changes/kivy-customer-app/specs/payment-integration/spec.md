# Payment Integration

E-specificação para integração com gateways de pagamento (Asaas, Mercado Pago).

## Purpose

Processar pagamentos de assinaturas e serviços avulsos de forma segura através de gateways externos, suportando PIX, cartão de crédito e boleto, sem manipular dados sensíveis diretamente no app.

## Requirements

### Requirement: Integração com Asaas
O sistema DEVE suportar Asaas como gateway primário para assinaturas.

#### Scenario: Criar cobrança de assinatura
- **WHEN** cliente assina plano
- **THEN** sistema cria cobrança recorrente no Asaas via API

#### Scenario: Webhook de pagamento aprovado
- **WHEN** Asaas confirma pagamento via webhook
- **THEN** sistema ativa assinatura e envia notificação

#### Scenario: Webhook de pagamento falhou
- **WHEN** Asaas notifica pagamento recusado
- **THEN** sistema marca assinatura como inadimplente e notifica cliente

### Requirement: Integração com Mercado Pago
O sistema DEVE suportar Mercado Pago como gateway secundário.

#### Scenario: Checkout transparente
- **WHEN** cliente seleciona Mercado Pago
- **THEN** sistema abre modal de pagamento sem sair do app

#### Scenario: PIX via Mercado Pago
- **WHEN** cliente escolhe PIX
- **THEN** sistema exibe QR Code e código copia-e-cola

#### Scenario: Aprovação automática PIX
- **WHEN** cliente paga PIX
- **THEN** sistema recebe confirmação em até 5 minutos

### Requirement: Cartão de crédito
O sistema DEVE aceitar cartões de crédito para pagamentos únicos e recorrentes.

#### Scenario: Salvar cartão
- **WHEN** cliente paga com cartão
- **THEN** sistema oferece opção "Salvar cartão para futuras compras"

#### Scenario: Pagamento recorrente
- **WHEN** é dia de renovação
- **THEN** sistema cobra cartão salvo automaticamente

#### Scenario: Atualizar cartão expirado
- **WHEN** cartão está expirando
- **THEN** sistema notifica cliente para atualizar dados

### Requirement: Boleto bancário
O sistema DEVE aceitar boleto para clientes sem cartão.

#### Scenario: Gerar boleto
- **WHEN** cliente seleciona boleto
- **THEN** sistema gera boleto com vencimento em 3 dias úteis

#### Scenario: Lembrete de vencimento
- **WHEN** faltam 2 dias para vencimento
- **THEN** sistema envia notificação "Seu boleto vence em 2 dias"

#### Scenario: Boleto pago
- **WHEN** cliente paga boleto
- **THEN** sistema recebe confirmação em até 1 dia útil

### Requirement: Histórico de pagamentos
O sistema DEVE exibir histórico completo de transações.

#### Scenario: Listar pagamentos
- **WHEN** cliente visualiza histórico
- **THEN** sistema mostra todas as transações com status

#### Scenario: Baixar recibo
- **WHEN** cliente clica em transação
- **THEN** sistema oferece download de recibo em PDF

#### Scenario: Reembolso
- **WHEN** cliente solicita reembolso dentro da política
- **THEN** sistema processa e notifica prazo de estorno