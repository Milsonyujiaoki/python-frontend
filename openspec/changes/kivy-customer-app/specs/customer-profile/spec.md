# Customer Profile

E-specificação para perfil do cliente no app mobile.

## Purpose

Centralizar informações do cliente, preferências, histórico e configurações em um perfil unificado, permitindo personalização da experiência e gestão da conta.

## Requirements

### Requirement: Cliente pode criar conta
O sistema DEVE permitir cadastro via email, telefone ou redes sociais.

#### Scenario: Cadastro com email
- **WHEN** cliente fornece email e senha
- **THEN** sistema envia email de verificação

#### Scenario: Cadastro com telefone
- **WHEN** cliente fornece telefone
- **THEN** sistema envia SMS com código de verificação

#### Scenario: Cadastro com Google
- **WHEN** cliente usa "Continuar com Google"
- **THEN** sistema importa nome, email e foto do perfil Google

### Requirement: Perfil editável
O sistema DEVE permitir edição de dados pessoais.

#### Scenario: Atualizar dados cadastrais
- **WHEN** cliente edita perfil
- **THEN** sistema permite alterar nome, telefone, data de nascimento

#### Scenario: Upload de foto de perfil
- **WHEN** cliente envia foto
- **THEN** sistema salva e exibe em todo o app

#### Scenario: Preferências de comunicação
- **WHEN** cliente configura preferências
- **THEN** sistema respeita opt-in/out para SMS, email, push

### Requirement: Histórico de agendamentos
O sistema DEVE exibir histórico completo de agendamentos.

#### Scenario: Histórico passado
- **WHEN** cliente visualiza histórico
- **THEN** sistema lista agendamentos passados com barbeiro e serviço

#### Scenario: Próximos agendamentos
- **WHEN** cliente tem agendamentos futuros
- **THEN** sistema exibe em destaque no topo

#### Scenario: Reagendar rápido
- **WHEN** cliente clica "Repetir agendamento"
- **THEN** sistema abre fluxo com barbeiro e serviço pré-selecionados

### Requirement: Lista de favoritos
O sistema DEVE permitir salvar barbeiros favoritos.

#### Scenario: Adicionar favorito
- **WHEN** cliente clica estrela em barbeiro
- **THEN** sistema salva na lista de favoritos

#### Scenario: Agendar com favorito
- **WHEN** cliente acessa favoritos
- **THEN** sistema exibe lista com horários disponíveis

### Requirement: Configurações da conta
O sistema DEVE permitir gestão de segurança e privacidade.

#### Scenario: Trocar senha
- **WHEN** cliente solicita troca de senha
- **THEN** sistema envia email com link de redefinição

#### Scenario: Excluir conta
- **WHEN** cliente solicita exclusão
- **THEN** sistema agenda exclusão em 7 dias e permite cancelar

#### Scenario: Exportar dados
- **WHEN** cliente solicita exportação
- **THEN** sistema gera arquivo JSON com todos os dados em 24h