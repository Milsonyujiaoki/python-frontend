# Loyalty Program

Especificação para sistema de fidelidade com pontos, níveis e recompensas.

## Purpose

Fidelizar clientes através de gamificação com pontos por cortes, níveis progressivos e resgate de benefícios, aumentando retenção e frequência de visitas.

## Requirements

### Requirement: Cliente ganha pontos por corte
O sistema DEVE atribuir pontos automaticamente após cada corte realizado.

#### Scenario: Ganho padrão de pontos
- **WHEN** cliente completa um corte
- **THEN** sistema creditada 10 pontos na conta do cliente

#### Scenario: Ganho no aniversário
- **WHEN** cliente realiza corte no mês de aniversário
- **THEN** sistema credita 50 pontos (bônus aniversário)

#### Scenario: Ganho por indicação
- **WHEN** cliente indicado realiza primeiro corte
- **THEN** sistema credita 100 pontos para quem indicou

### Requirement: Sistema de níveis progressivos
O sistema DEVE classificar clientes em 4 níveis baseados em pontos acumulados.

#### Scenario: Nível Bronze (0-99 pontos)
- **WHEN** cliente tem 0-99 pontos
- **THEN** nível exibido é "Bronze" com badge cinza

#### Scenario: Nível Silver (100-299 pontos)
- **WHEN** cliente atinge 100 pontos
- **THEN** nível muda para "Silver" com desbloqueio de 5% desconto

#### Scenario: Nível Gold (300-599 pontos)
- **WHEN** cliente atinge 300 pontos
- **THEN** nível muda para "Gold" com desbloqueio de 10% desconto + prioridade

#### Scenario: Nível Platinum (600+ pontos)
- **WHEN** cliente atinge 600 pontos
- **THEN** nível muda para "Platinum" com 20% desconto + agendamento prioritário + brinde mensal

### Requirement: Cliente visualiza progresso
O sistema DEVE exibir barra de progresso, pontos atuais e próximo nível.

#### Scenario: Visualizar pontos atuais
- **WHEN** cliente acessa tela de fidelidade
- **THEN** sistema mostra pontos totais, nível atual e barra de progresso

#### Scenario: Próximo benefício
- **WHEN** cliente está a 20 pontos do próximo nível
- **THEN** sistema exibe "Faltam 20 pts para Silver e 5% OFF"

### Requirement: Resgate de cupons
O sistema DEVE permitir resgate de pontos por cupons de desconto.

#### Scenario: Resgatar cupom de 10% OFF
- **WHEN** cliente tem 200 pontos e resgata cupom
- **THEN** sistema debita 200 pontos e gera código cupom

#### Scenario: Cupom expirado
- **WHEN** cliente tenta usar cupom após validade (30 dias)
- **THEN** sistema rejeita e informa data de expiração

#### Scenario: Histórico de resgates
- **WHEN** cliente visualiza histórico
- **THEN** sistema lista cupons resgatados com status (usado/disponível/expirado)

### Requirement: Badges e conquistas
O sistema DEVE conceder badges por marcos especiais.

#### Scenario: Badge "Primeiro Corte"
- **WHEN** cliente completa primeiro agendamento
- **THEN** sistema concede badge e exibe pop-up de conquista

#### Scenario: Badge "Freguês Frequente"
- **WHEN** cliente realiza 10 cortes no mês
- **THEN** sistema concede badge + 50 pontos bônus

#### Scenario: Badge "Aniversariante"
- **WHEN** cliente realiza corte no dia do aniversário
- **THEN** sistema concede badge especial + 100 pontos