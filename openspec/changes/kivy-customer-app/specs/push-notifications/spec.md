# Push Notifications

Especificação para sistema de notificações push no app mobile.

## Purpose

Engajar clientes com notificações relevantes de lembretes, promoções e conquistas, reduzindo no-shows e aumentando retenção através de comunicação proativa.

## Requirements

### Requirement: Notificações de agendamento
O sistema DEVE enviar notificações para lembretes de agendamentos.

#### Scenario: Lembrete 24h antes
- **WHEN** faltam 24h para agendamento
- **THEN** sistema envia push "Seu horário é amanhã às {HH:MM} com {barbeiro}"

#### Scenario: Lembrete 2h antes
- **WHEN** faltam 2h para agendamento
- **THEN** sistema envia push com ações "Confirmar" e "Cancelar"

#### Scenario: Agendamento confirmado
- **WHEN** cliente agenda horário
- **THEN** sistema envia push "Agendamento confirmado para {data} às {HH:MM}"

### Requirement: Notificações de marketing
O sistema DEVE enviar promoções e novidades respeitando preferências.

#### Scenario: Promoção aniversário
- **WHEN** é aniversário do cliente
- **THEN** sistema envia push "Feliz aniversário! 20% OFF hoje"

#### Scenario: Retorno após inatividade
- **WHEN** cliente não agenda há 30 dias
- **THEN** sistema envia push "Saudades! Agende hoje com 15% OFF"

#### Scenario: Opt-out respeitado
- **WHEN** cliente desativou marketing
- **THEN** sistema não envia notificações promocionais

### Requirement: Notificações de gamificação
O sistema DEVE notificar sobre conquistas e progresso de nível.

#### Scenario: Novo nível alcançado
- **WHEN** cliente atinge novo nível
- **THEN** sistema envia push com celebração e novos benefícios

#### Scenario: Badge conquistado
- **WHEN** cliente completa conquista
- **THEN** sistema envia push "Você ganhou o badge {nome}!"

####Scenario: Quase lá
- **WHEN** cliente está a 10 pontos do próximo nível
- **THEN** sistema envia push "Faltam 10 pts para {nível} e {benefício}"

### Requirement: Notificações de sistema
O sistema DEVE informar sobre atualizações e mudanças relevantes.

#### Scenario: Assinatura renovada
- **WHEN** assinatura é renovada com sucesso
- **THEN** sistema envia push "Assinatura renovada! Próxima cobrança em {data}"

#### Scenario: Pagamento pendente
- **WHEN** pagamento de assinatura falhou
- **THEN** sistema envia push "Pagamento pendente. Atualize seus dados."

#### Scenario: Novo barbeiro
- **WHEN** barbeiro entra na equipe
- **THEN** sistema envia push "Conheça {nome}, nosso novo especialista em {especialidade}"

### Requirement: Gestão de preferências
O sistema DEVE permitir controle granular de notificações.

#### Scenario: Desativar categorias
- **WHEN** cliente acessa configurações
- **THEN** sistema permite toggle para "Lembretes", "Promoções", "Conquistas"

#### Scenario: Horário de silêncio
- **WHEN** cliente configura "Não perturbe"
- **THEN** sistema silencia notificações no período definido

#### Scenario: Reset de preferências
- **WHEN** cliente clica "Restaurar padrão"
- **THEN** sistema reativa todas as notificações