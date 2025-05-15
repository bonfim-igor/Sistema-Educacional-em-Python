# Sistema Educacional em Python

Este projeto é um sistema educacional desenvolvido em Python, que oferece uma plataforma básica para gerenciamento de usuários, cursos, avaliações e acessos.
O sistema utiliza arquivos JSON para armazenar dados, possui autenticação segura com hash de senhas e oferece menus interativos via terminal.

---

## Requisitos para Rodar o Sistema

- Python 3.7 ou superior
- Bibliotecas Python:
  - `bcrypt` (para segurança das senhas)
  - `matplotlib` (para geração de gráficos das estatísticas)
- Sistema operacional compatível com Python (Windows, Linux, macOS)

---

### Funcionalidades do Usuário

- **Cadastro de usuário:** Criação de conta com validação de dados (usuário, senha, idade e gênero).
- **Login:** Autenticação segura com verificação de senha via bcrypt.
- **Visualizar cursos:** Navegar pelos cursos disponíveis organizados por nível (iniciante, intermediário, avançado).
- **Avaliar cursos:** Avaliar cursos já acessados, com notas de 1 a 5.
- **Visualizar avaliações:** Consultar estatísticas das avaliações feitas nos cursos.
- **Gerenciar conta:** Excluir a própria conta com confirmação e backup automático.
- **Registro de acessos:** O sistema registra a quantidade de acessos e o tempo gasto nos cursos, para gerar estatísticas.

### Funcionalidades do Administrador

- **Gerenciamento completo de usuários:** Visualizar, cadastrar, editar e remover usuários.
- **Gerenciamento de cursos:** Criar, editar e excluir cursos, incluindo organização por níveis de dificuldade.
- **Visualização de estatísticas detalhadas:** Estatísticas sobre usuários (idade, gênero), acessos (quantidade, tempo médio) e avaliações.
- **Backups automáticos:** Geração de backups dos arquivos JSON para proteção dos dados.
- **Logs de operações:** Registro das operações importantes realizadas no sistema para auditoria.

---

### Estrutura do Projeto

- `main.py` – Arquivo principal que inicia o sistema.
- `usuario.json` – Dados dos usuários cadastrados.
- `cursos.json` – Dados dos cursos disponíveis.
- `avaliacoes.json` – Registro das avaliações feitas.
- `acessos.json` – Dados sobre acessos e tempo de uso.
- `backups/` – Pasta para backups automáticos dos arquivos JSON.
- `log_usuario.log` – Registro das operações importantes do sistema.
