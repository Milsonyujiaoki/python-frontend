# Photo Gallery

E-specificação para galeria privada de fotos dos cortes do cliente.

## Purpose

Permitir que clientes registrem e visualizem seus cortes em uma galeria privada organizada por barbeiro e data, facilitando referência para futuros agendamentos e construção de histórico visual.

## Requirements

### Requirement: Cliente pode upload de fotos
O sistema DEVE permitir upload de fotos após corte realizado.

#### Scenario: Upload após corte
- **WHEN** corte é marcado como concluído
- **THEN** sistema oferece opção "Adicionar foto" por 24h

#### Scenario: Múltiplas fotos
- **WHEN** cliente envia fotos
- **THEN** sistema permite até 5 fotos por corte gratuitamente

#### Scenario: Compressão de imagens
- **WHEN** cliente envia foto > 5MB
- **THEN** sistema comprime automaticamente para máximo 2MB

### Requirement: Galeria organizada por barbeiro
O sistema DEVE permitir filtragem de fotos por barbeiro que realizou o corte.

#### Scenario: Ver fotos por barbeiro
- **WHEN** cliente seleciona barbeiro na galeria
- **THEN** sistema exibe apenas cortes feitos por aquele barbeiro

#### Scenario: Timeline cronológica
- **WHEN** cliente visualiza galeria completa
- **THEN** sistema ordena fotos do mais recente para o mais antigo

### Requirement: Galeria privada
O sistema DEVE garantir que fotos sejam visíveis apenas pelo cliente dono.

#### Scenario: Acesso próprio
- **WHEN** cliente autentica e acessa galeria
- **THEN** sistema exibe todas as fotos do cliente

#### Scenario: Acesso negado
- **WHEN** usuário tenta acessar galeria de outro cliente
- **THEN** sistema retorna erro 403 Forbidden

#### Scenario: Barbeiro visualiza
- **WHEN** barbeiro acessa perfil do cliente
- **THEN** sistema permite visualizar fotos para referência

### Requirement: Cache offline
O sistema DEVE cachear fotos localmente para visualização offline.

#### Scenario: Cache de thumbnails
- **WHEN** cliente abre galeria online
- **THEN** sistema salva thumbnails em cache local

#### Scenario: Visualização offline
- **WHEN** cliente abre galeria sem conexão
- **THEN** sistema exibe fotos cacheadas com indicador "offline"

#### Scenario: Sync ao reconectar
- **WHEN** cliente reconecta após upload offline
- **THEN** sistema envia fotos pendentes em background

### Requirement: Compartilhar foto
O sistema DEVE permitir compartilhar foto em redes sociais.

#### Scenario: Compartilhar no Instagram
- **WHEN** cliente clica "Compartilhar"
- **THEN** sistema abre Intent com foto e watermark da barbearia

#### Scenario: Compartilhar sem watermark
- **WHEN** cliente é nível Platinum
- **THEN** sistema permite compartilhar sem watermark

#### Scenario: Foto privada não compartilhável
- **WHEN** cliente marca foto como "privada"
- **THEN** opção de compartilhar é desabilitada