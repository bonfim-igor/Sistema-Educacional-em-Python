### Sistema Educacional em Python
Este projeto é um sistema educacional desenvolvido em Python, que oferece uma plataforma básica para gerenciamento de usuários, cursos, avaliações e acessos. O sistema utiliza arquivos JSON para armazenar dados, possui autenticação segura com hash de senhas e oferece menus interativos via terminal.

---

### 📋 Requisitos para Rodar o Sistema

- Python 3.7 ou superior
- Bibliotecas Python:
- bcrypt (para segurança das senhas)
- matplotlib (para geração de gráficos das estatísticas)
- Sistema operacional compatível com Python (Windows, Linux, macOS)

---

### 🔐 Credenciais de Acesso Administrador

- Usuário: admin
- Senha: admin123

---

### 👤 Funcionalidades do Usuário

- Cadastro de Usuário
- Criação de conta com validação de dados (usuário, senha, idade e gênero).
- Login
- Autenticação segura com hash de senha utilizando bcrypt.
- Acesso ao Sistema
- Visualização de cursos disponíveis.
- Realização de avaliações.
- Acompanhamento de desempenho individual.

---

### 🛠️ Funcionalidades do Administrador

- Gerenciamento de Usuários
- Listagem de todos os usuários cadastrados.
- Edição e exclusão de contas de usuários.
- Gerenciamento de Cursos
- Criação, edição e exclusão de cursos.
- Análise de Desempenho
- Geração de relatórios estatísticos utilizando matplotlib.

---

### Estrutura do Projeto

- `main.py` – Arquivo principal que inicia o sistema.
- `usuario.json` – Dados dos usuários cadastrados.
- `cursos.json` – Dados dos cursos disponíveis.
- `avaliacoes.json` – Registro das avaliações feitas.
- `acessos.json` – Dados sobre acessos e tempo de uso.
- `backups/` – Pasta para backups automáticos dos arquivos JSON.
- `log_usuario.log` – Registro das operações importantes do sistema.
