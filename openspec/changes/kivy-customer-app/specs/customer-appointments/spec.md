# Customer Appointments

Especificação para agendamento de horários no app mobile do cliente.

## Purpose

Permitir que clientes agendem, remarquem e cancelem horários com barbeiros específicos através do app mobile, com confirmação em tempo real e lembretes automáticos.

## Requirements

### Requirement: Cliente pode visualizar barbeiros disponíveis
O sistema DEVE exibir lista de barbeiros ativos com especialidade, avaliação e horários disponíveis.

#### Scenario: Listar barbeiros com filtro de data
- **WHEN** cliente seleciona uma data no agendador
- **THEN** sistema exibe barbeiros com horários livres naquele dia

#### Scenario: Exibir informações do barbeiro
- **WHEN** cliente visualiza lista de barbeiros
- **THEN** sistema mostra nome, especialidade, rating (estrelas) e foto

### Requirement: Cliente pode agendar horário
O sistema DEVE permitir agendamento com seleção de barbeiro, serviço, data e horário.

#### Scenario: Agendamento bem-sucedido
- **WHEN** cliente seleciona barbeiro, serviço, data e horário disponíveis
- **THEN** sistema confirma agendamento e envia notificação

#### Scenario: Conflito de horário
- **WHEN** cliente tenta agendar horário já ocupado
- **THEN** sistema exibe erro e sugere horários alternativos

#### Scenario: Agendamento mínimo antecipado
- **WHEN** cliente tenta agendar com menos de 30 minutos de antecedência
- **THEN** sistema bloqueia e informa tempo mínimo necessário

### Requirement: Cliente pode cancelar agendamento
O sistema DEVE permitir cancelamento com até 24h de antecedência sem penalidade.

#### Scenario: Cancelamento dentro do prazo
- **WHEN** cliente cancela com mais de 24h de antecedência
- **THEN** sistema cancela sem penalidade e libera horário

#### Scenario: Cancelamento fora do prazo
- **WHEN** cliente cancela com menos de 24h de antecedência
- **THEN** sistema aplica advertência e perde pontos de fidelidade

#### Scenario: Múltiplos cancelamentos
- **WHEN** cliente cancela 3 vezes no mês
- **THEN** sistema bloqueia agendamento online por 7 dias

### Requirement: Cliente recebe lembretes
O sistema DEVE enviar lembretes push e SMS para agendamentos confirmados.

#### Scenario: Lembrete 24h antes
- **WHEN** agendamento está confirmado para daqui a 24h
- **THEN** sistema envia push notification "Seu horário é amanhã às {HH:MM}"

#### Scenario: Lembrete 2h antes
- **WHEN** agendamento está confirmado para daqui a 2h
- **THEN** sistema envia push notification "Seu horário é hoje às {HH:MM}"

#### Scenario: Confirmação de presença
- **WHEN** cliente recebe lembrete de 2h
- **THEN** sistema oferece botões "Confirmar" e "Cancelar"