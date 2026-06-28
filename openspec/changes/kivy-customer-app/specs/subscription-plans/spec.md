# Subscription Plans

Especificação para planos de assinatura recorrente de cortes.

## Purpose

Oferecer planos mensais, trimestrais, semestrais e anuais de cortes com cobrança automática via gateway de pagamento, garantindo receita recorrente e fidelidade do cliente.

## Requirements

### Requirement: Cliente pode assinar plano
O sistema DEVE oferecer 4 planos com preços progressivamente menores por compromisso maior.

#### Scenario: Plano Mensal
- **WHEN** cliente assina plano mensal
- **THEN** sistema cobra valor X/mês com direito a 4 cortes/mês

#### Scenario: Plano Trimestral
- **WHEN** cliente assina plano trimestral
- **THEN** sistema cobra valor Y/trimestre (10% desconto vs mensal) com 12 cortes

#### Scenario: Plano Semestral
- **WHEN** cliente assina plano semestral
- **THEN** sistema cobra valor Z/semestre (15% desconto vs mensal) com 24 cortes

#### Scenario: Plano Anual
- **WHEN** cliente assina plano anual
- **THEN** sistema cobra valor W/ano (20% desconto vs mensal) com 48 cortes

### Requirement: Gestão de assinatura
O sistema DEVE permitir-cancelamento e alteração de plano.

#### Scenario: Cancelar assinatura
- **WHEN** cliente cancela assinatura
- **THEN** sistema mantém acesso até fim do período pago, não renova

#### Scenario: Upgrade de plano
- **WHEN** cliente upgrade de mensal para anual
- **THEN** sistema cobra diferença proporcional e aplica novo preço

#### Scenario: Downgrade de plano
- **WHEN** cliente faz downgrade de anual para mensal
- **THEN** sistema credita saldo proporcional e aplica novo preço no próximo ciclo

### Requirement: Renovação automática
O sistema DEVE renovar automaticamente assinaturas ativas.

#### Scenario: Renovação bem-sucedida
- **WHEN** cartão está válido e tem saldo
- **THEN** sistema renova assinatura e envia recibo

#### Scenario: Renovação falhou
- **WHEN** cartão foi recusado
- **THEN** sistema notifica cliente e mantém 7 dias de carência

#### Scenario: Lembrete de renovação
- **WHEN** faltam 3 dias para renovação
- **THEN** sistema envia notificação "Sua assinatura renova em 3 dias"

### Requirement: Uso de cortes do plano
O sistema DEVE contabilizar cortes usados vs disponíveis no plano.

#### Scenario: Agendar corte com plano
- **WHEN** cliente tem plano ativo e cortes disponíveis
- **THEN** sistema permite agendamento sem cobrança adicional

#### Scenario: Excedeu plano
- **WHEN** cliente usou todos os cortes do mês
- **THEN** sistema cobra preço normal do serviço

#### Scenario: Saldo visualização
- **WHEN** cliente visualiza detalhes do plano
- **THEN** sistema mostra "2/4 cortes usados este mês"