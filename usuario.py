from datetime import datetime
import shutil
import json
import os
import logging
import bcrypt

USUARIO_ARQUIVO = "usuario.json"
CURSO_ARQUIVO = "cursos.json"
ACESSO_ARQUIVO = "acessos.json"
AVALIACOES_ARQUIVO = "avaliacoes.json"
BACKUP_PASTA = "backups"

LOG_USUARIO = "log_usuario.log"

# Configuração do logger
logger_usuario = logging.getLogger('usuario')
logger_usuario.setLevel(logging.INFO)
file_handler_usuario = logging.FileHandler(LOG_USUARIO)
file_handler_usuario.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger_usuario.addHandler(file_handler_usuario)


def hash_senha(senha: str) -> str:
    """
    Gera o hash bcrypt da senha para armazenamento seguro.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verificar_senha(senha: str, hashed: str) -> bool:
    """
    Verifica se a senha informada confere com o hash armazenado.
    """
    try:
        return bcrypt.checkpw(senha.encode('utf-8'), hashed.encode('utf-8'))
    except ValueError:
        return False


def carregar_dados(arquivo: str):
    """
    Carrega dados de um arquivo JSON, retorna lista vazia se não existir ou inválido.
    """
    if os.path.exists(arquivo):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            logger_usuario.warning(f"Falha ao carregar dados do arquivo {arquivo}.")
            return []
    return []


def salvar_dados(arquivo: str, dados):
    """
    Salva dados formatados em JSON no arquivo especificado.
    """
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)


def criar_backup():
    """
    Cria pasta de backups se não existir.
    """
    if not os.path.exists(BACKUP_PASTA):
        os.makedirs(BACKUP_PASTA)


def backup_arquivo(origem: str):
    """
    Cria backup do arquivo JSON na pasta de backups com timestamp.
    """
    criar_backup()
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_backup = os.path.join(BACKUP_PASTA, f"backup_{os.path.basename(origem).replace('.json','')}_{data_hora}.json")
    try:
        shutil.copy(origem, nome_backup)
        logger_usuario.info(f"Backup criado: {nome_backup}")
        print(f"Backup criado: {nome_backup}")
    except Exception as e:
        logger_usuario.error(f"Erro ao criar backup do arquivo {origem}: {e}")
        print(f"Erro ao criar backup: {e}")


def cadastrar_usuario():
    """
    Realiza o cadastro de um novo usuário com validações e confirmação de senha.
    """
    usuarios = carregar_dados(USUARIO_ARQUIVO)

    usuario = input("Informe o usuário (mínimo 3 caracteres, sem espaços): ").strip()
    if len(usuario) < 3 or " " in usuario:
        print("Usuário inválido. Tente novamente.\n")
        return

    # Verifica duplicidade
    if any(u["usuario"] == usuario for u in usuarios):
        print("Usuário já cadastrado.\n")
        return

    senha = input("Informe a senha (mínimo 6 caracteres): ").strip()
    if len(senha) < 6:
        print("Senha muito curta.\n")
        return

    confirma = input("Confirme a senha: ").strip()
    if senha != confirma:
        print("Senhas não conferem.\n")
        return

    genero = input("Gênero (masculino/feminino): ").strip().lower()
    if genero not in ["masculino", "feminino"]:
        print("Gênero inválido.\n")
        return

    novo = {
        "usuario": usuario,
        "senha": hash_senha(senha),
        "tipo": "usuario",
        "genero": genero
    }

    usuarios.append(novo)
    salvar_dados(USUARIO_ARQUIVO, usuarios)
    logger_usuario.info(f"Usuário '{usuario}' cadastrado.")
    print("Cadastro realizado com sucesso.\n")


def autenticar_usuario():
    """
    Autentica usuário comparando hash da senha e chama o menu do usuário autenticado.
    """
    usuarios = carregar_dados(USUARIO_ARQUIVO)

    while True:
        usuario = input("Informe o usuário: ").strip()
        senha = input("Informe a senha: ").strip()

        user = next((u for u in usuarios if u["usuario"] == usuario), None)
        if user and verificar_senha(senha, user["senha"]):
            logger_usuario.info(f"Usuário '{usuario}' autenticado.")
            print(f"Bem-vindo, {usuario}!\n")
            menu_usuario_autenticado(user)
            return
        else:
            print("Credenciais inválidas.\n")


def ver_cursos(usuario):
    """
    Exibe cursos por nível e registra o acesso do usuário.
    """
    cursos = carregar_dados(CURSO_ARQUIVO)
    if not cursos:
        print("Nenhum curso disponível.\n")
        return

    niveis = ["iniciante", "intermediário", "avançado"]

    while True:
        print("\n=== MENU DE CURSOS ===")
        print("[1] Cursos Iniciante")
        print("[2] Cursos Intermediário")
        print("[3] Cursos Avançado")
        print("[4] Voltar ao menu principal")
        opcao = input("Escolha uma opção entre (1-4): ").strip()

        if opcao == "4":
            break
        if opcao not in ["1", "2", "3"]:
            print("Opção inválida.\n")
            continue

        nivel = niveis[int(opcao) - 1]
        cursos_nivel = [c for c in cursos if c["nivel"] == nivel]

        if not cursos_nivel:
            print(f"Não há cursos cadastrados para o nível {nivel}.\n")
            continue

        while True:
            print(f"\n=== CURSOS NÍVEL {nivel.upper()} ===")
            for idx, curso in enumerate(cursos_nivel, 1):
                print(f"[{idx}] {curso['nome']}")
            print(f"[{len(cursos_nivel) + 1}] Voltar")

            escolha = input("Escolha um curso para ver o conteúdo: ").strip()

            if escolha == str(len(cursos_nivel) + 1):
                break

            if not escolha.isdigit() or not (1 <= int(escolha) <= len(cursos_nivel)):
                print("Opção inválida.\n")
                continue

            curso_selecionado = cursos_nivel[int(escolha) - 1]
            print(f"\nConteúdo do curso '{curso_selecionado['nome']}':")
            print(curso_selecionado['conteudo'])
            input("\nPressione Enter para voltar ao menu de cursos.")

    acessos = carregar_dados(ACESSO_ARQUIVO)
    acessos.append({"usuario": usuario["usuario"], "curso_count": len(cursos), "timestamp": datetime.now().isoformat()})
    salvar_dados(ACESSO_ARQUIVO, acessos)


def avaliar_curso(usuario):
    """
    Permite o usuário avaliar um curso e registra a avaliação.
    """
    cursos = carregar_dados(CURSO_ARQUIVO)
    if not cursos:
        print("Nenhum curso disponível para avaliação.\n")
        return

    print("\nCursos disponíveis para avaliação:")
    for i, curso in enumerate(cursos):
        print(f"[{i+1}] {curso['nome']}")

    try:
        escolha = int(input("Escolha o número do curso que deseja avaliar: "))
        if not (1 <= escolha <= len(cursos)):
            print("Curso inválido.\n")
            return
    except ValueError:
        print("Entrada inválida.\n")
        return

    curso_escolhido = cursos[escolha - 1]
    nome_curso = curso_escolhido["nome"]
    nivel_curso = curso_escolhido.get("nivel", "não especificado")

    avaliacoes = carregar_dados(AVALIACOES_ARQUIVO)
    if any(av["usuario"] == usuario["usuario"] and av["curso"] == nome_curso for av in avaliacoes):
        print("Você já avaliou este curso.\n")
        return

    try:
        nota = int(input("Avalie de 1 a 5: "))
        if not (1 <= nota <= 5):
            print("Nota fora do intervalo.\n")
            return
    except ValueError:
        print("Nota inválida.\n")
        return

    avaliacoes.append({
        "usuario": usuario["usuario"],
        "curso": nome_curso,
        "nivel": nivel_curso,
        "nota": nota,
        "timestamp": datetime.now().isoformat()
    })

    salvar_dados(AVALIACOES_ARQUIVO, avaliacoes)
    print("Avaliação registrada com sucesso.\n")


def deletar_usuario(usuario):
    """
    Exclui a conta do usuário com confirmação e backup antes.
    """
    confirm = input(f"Tem certeza que deseja excluir a conta '{usuario['usuario']}'? (s/n): ").strip().lower()
    if confirm != "s":
        print("Exclusão cancelada.\n")
        return

    backup_arquivo(USUARIO_ARQUIVO)

    usuarios = carregar_dados(USUARIO_ARQUIVO)
    usuarios = [u for u in usuarios if u["usuario"] != usuario["usuario"]]
    salvar_dados(USUARIO_ARQUIVO, usuarios)
    logger_usuario.info(f"Usuário '{usuario['usuario']}' excluído.")
    print("Conta excluída com sucesso.\n")


def menu_usuario_autenticado(usuario):
    """
    Menu principal para usuários autenticados.
    """
    while True:
        print("=== MENU USUÁRIO ===")
        print("[1] Ver cursos")
        print("[2] Avaliar curso")
        print("[3] Excluir minha conta")
        print("[4] Logout")
        opcao = input("Escolha uma opção entre (1-4): ").strip()

        if opcao == "1":
            ver_cursos(usuario)
        elif opcao == "2":
            avaliar_curso(usuario)
        elif opcao == "3":
            deletar_usuario(usuario)
            break
        elif opcao == "4":
            print("Logout realizado.\n")
            break
        else:
            print("Opção inválida.\n")


def menu_usuario():
    """
    Menu inicial para usuários não autenticados.
    """
    while True:
        print("=== MENU INICIAL ===")
        print("[1] Cadastrar")
        print("[2] Login")
        print("[3] Sair")
        opcao = input("Escolha entre (1-3): ").strip()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            autenticar_usuario()
        elif opcao == "3":
            print("Saindo do sistema.\n")
            break
        else:
            print("Opção inválida.\n")


if __name__ == "__main__":
    menu_usuario()