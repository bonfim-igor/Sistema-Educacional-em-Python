# Sistema Educacional em Python

Este projeto é um sistema educacional simples em Python dividido em arquivos py, json e log.

---

## Requisitos

- Python 3.6 ou superior
- Biblioteca `bcrypt`
- Biblioteca `matplotlib`

---

## Funcionalidades de Admin

### 1. Autenticação do Administrador
- Solicita usuário e senha (senha oculta no input).
- Limite de 3 tentativas.
- Verificação da senha usando hash SHA-256.
- Registra logs de tentativas e acessos no arquivo `log_admin.log`.

### 2. Cadastro de Cursos
- Cadastro de novos cursos com nome, nível (iniciante, intermediário, avançado) e conteúdo.
- Limite de até 7 cursos por nível.
- Conteúdo do curso limitado a 5000 caracteres para evitar abusos.
- Validação para evitar nomes duplicados de cursos.
- Salva os dados em formato JSON (`cursos.json`).

### 3. Visualização de Cursos
- Exibe lista de cursos organizados por nível.
- Permite visualizar o conteúdo completo de cada curso.

### 4. Edição de Cursos
- Permite alterar nome, conteúdo e nível de um curso existente.
- Mantém validações de limite e evita duplicidade de nomes.
- Atualiza o arquivo JSON com as modificações.

### 5. Exclusão de Cursos
- Permite excluir cursos cadastrados.
- Solicita confirmação para evitar exclusões acidentais.

### 6. Estatísticas Gerais
- Mostra estatísticas da plataforma:
  - Total de usuários cadastrados
  - Total de cursos cadastrados
  - Total de acessos realizados
  - Total de avaliações feitas
  - Distribuição de usuários por gênero (respeitando a privacidade)

---

## Funcionalidades de Usuário

### 1. Cadastro de Usuário
- Permite criar um novo usuário com validação de nome (mínimo 3 caracteres, sem espaços) e senha (mínimo 6 caracteres).
- Gênero do usuário deve ser informado (masculino ou feminino).
- Senhas são armazenadas de forma segura utilizando hash bcrypt.
- Evita cadastro duplicado de usuários.

### 2. Autenticação
- Usuário pode fazer login com nome e senha.
- A senha é verificada contra o hash armazenado.
- Após autenticação, o usuário acessa um menu específico com opções adicionais.

### 3. Visualização de Cursos
- Exibe cursos disponíveis organizados por nível (iniciante, intermediário, avançado).
- Permite navegar e visualizar o conteúdo dos cursos.
- Registra os acessos do usuário para fins de controle.

### 4. Avaliação de Cursos
- Usuário pode avaliar um curso com nota de 1 a 5.
- Cada usuário pode avaliar um curso apenas uma vez.
- Avaliações são registradas com informações do usuário, curso, nível, nota e timestamp.

### 5. Exclusão de Conta
- Usuário pode excluir sua conta após confirmação.
- Antes da exclusão, é criado um backup do arquivo de usuários.
- Exclusão remove os dados do usuário do arquivo JSON.

### 6. Gerenciamento de Dados e Backups
- Dados de usuários, cursos, acessos e avaliações são armazenados em arquivos JSON.
- Função para criação de backups automáticos dos arquivos JSON antes de operações sensíveis.
- Uso de logs para registrar eventos importantes do sistema.
