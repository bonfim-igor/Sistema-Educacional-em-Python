from utils.estatisticas import gerar_estatisticas_usuarios, gerar_estatisticas_acessos, gerar_estatisticas_avaliacoes
import json
import hashlib
import os
import logging
import getpass

USUARIO_ARQUIVO = "data/usuario.json"
CURSO_ARQUIVO = "data/cursos.json"
ACESSO_ARQUIVO = "data/acessos.json"
AVALIACOES_ARQUIVO = "data/avaliacoes.json"
MAX_CONTEUDO_CURSO = 5000

ADMIN_USUARIO = "admin"
ADMIN_SENHA = "admin123"
ADMIN_SENHA_HASH = hashlib.sha256(ADMIN_SENHA.encode()).hexdigest()

LOG_ADMIN = "logs/log_admin.log"

# Logger para admin: grava apenas eventos operacionais, sem dados pessoais sensíveis,
# para estar em conformidade com LGPD (ex: não grava senhas, só ações do admin).
logger_admin = logging.getLogger('admin')
logger_admin.setLevel(logging.INFO)
file_handler_admin = logging.FileHandler(LOG_ADMIN)
file_handler_admin.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger_admin.addHandler(file_handler_admin)

def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_dados(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)

def autenticar_admin():
    tentativas = 0
    max_tentativas = 3

    while tentativas < max_tentativas:
        usuario = input("Informe o usuário: ")
        senha = getpass.getpass("Informe a senha: ")  # senha oculta

        if usuario == ADMIN_USUARIO and hashlib.sha256(senha.encode()).hexdigest() == ADMIN_SENHA_HASH:
            print("Acesso concedido ao admin.\n")
            logger_admin.info(f"Admin '{usuario}' logado.")
            return True

        else:
            print("Credenciais incorretas.\n")
            logger_admin.warning("Tentativa de login admin inválida.")
            tentativas += 1
            print(f"Tentativas restantes: {max_tentativas - tentativas}\n")

    print("Número máximo de tentativas excedido. Encerrando acesso.")
    return False

def cadastrar_curso():
    cursos = carregar_dados(CURSO_ARQUIVO)

    print("\nNíveis disponíveis:")
    print("[1] Iniciante")
    print("[2] Intermediário")
    print("[3] Avançado")

    nivel_opcao = input("Escolha o nível do curso (1/2/3): ").strip()

    niveis = {"1": "iniciante", "2": "intermediário", "3": "avançado"}
    nivel = niveis.get(nivel_opcao)

    if not nivel:
        print("Nível inválido. Curso não cadastrado.")
        return

    cursos_nivel = [c for c in cursos if c["nivel"] == nivel]
    if len(cursos_nivel) >= 7:
        print(f"Limite de 7 cursos para o nível '{nivel}' já atingido.")
        return

    nome = input("Nome do curso: ").strip()

    if any(c["nome"].lower() == nome.lower() for c in cursos):
        print("Curso já cadastrado.")
        return

    print("Digite o conteúdo do curso (Digite salvar curso em uma linha vazia para finalizar):")
    conteudo = []
    total_chars = 0
    while True:
        linha = input()
        if linha == "salvar curso":
            break
        total_chars += len(linha)
        if total_chars > MAX_CONTEUDO_CURSO:
            print("Conteúdo do curso muito grande. Salvando curso até aqui.")
            break
        conteudo.append(linha)
    conteudo = "\n".join(conteudo)

    novo_curso = {
        "nome": nome,
        "conteudo": conteudo,
        "nivel": nivel
    }

    cursos.append(novo_curso)
    salvar_dados(CURSO_ARQUIVO, cursos)
    logger_admin.info(f"Curso cadastrado: {nome} ({nivel})")
    print(f"Curso '{nome}' cadastrado com sucesso no nível {nivel}.\n")


def ver_cursos():
    cursos = carregar_dados(CURSO_ARQUIVO)

    if not cursos:
        print("Nenhum curso cadastrado.")
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
            print("Opção inválida.")
            continue

        nivel = niveis[int(opcao) - 1]
        cursos_nivel = [c for c in cursos if c["nivel"] == nivel]

        if not cursos_nivel:
            print(f"Não há cursos cadastrados para o nível {nivel}.")
            continue

        while True:
            print(f"\n=== CURSOS NÍVEL {nivel.upper()} ===")
            for idx, curso in enumerate(cursos_nivel, 1):
                print(f"[{idx}] {curso['nome']}")
            print(f"[{len(cursos_nivel) + 1}] Voltar")

            escolha = input("Escolha um curso para ver o conteúdo: ").strip()

            if escolha == str(len(cursos_nivel) + 1):
                break

            if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(cursos_nivel):
                print("Opção inválida.")
                continue

            curso_selecionado = cursos_nivel[int(escolha) - 1]
            print(f"\nConteúdo do curso '{curso_selecionado['nome']}':")
            print(curso_selecionado['conteudo'])
            input("\nPressione Enter para voltar ao menu de cursos.")


def editar_curso():
    cursos = carregar_dados(CURSO_ARQUIVO)

    if not cursos:
        print("Nenhum curso cadastrado para editar.")
        return

    print("\n=== Editar Curso ===")
    for idx, curso in enumerate(cursos, 1):
        print(f"[{idx}] {curso['nome']} (Nível: {curso['nivel']})")
    print(f"[{len(cursos) + 1}] Cancelar")

    escolha = input("Escolha o curso que deseja editar: ").strip()

    if escolha == str(len(cursos) + 1):
        print("Edição cancelada.")
        return

    if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(cursos):
        print("Opção inválida.")
        return

    idx_curso = int(escolha) - 1
    curso = cursos[idx_curso]

    print(f"Editando curso '{curso['nome']}'")

    novo_nome = input(f"Novo nome (deixe vazio para manter '{curso['nome']}'): ").strip()
    if novo_nome:
        # Verifica duplicidade
        if any(c["nome"].lower() == novo_nome.lower() and c != curso for c in cursos):
            print("Já existe um curso com esse nome. Edição cancelada.")
            return
        curso["nome"] = novo_nome

    print("Digite o novo conteúdo do curso (Digite salvar curso em uma linha vazia para finalizar):")
    conteudo = []
    total_chars = 0
    while True:
        linha = input()
        if linha == "salvar curso":
            break
        total_chars += len(linha)
        if total_chars > MAX_CONTEUDO_CURSO:
            print("Conteúdo do curso muito grande. Salvando conteúdo até aqui.")
            break
        conteudo.append(linha)
    if conteudo:
        curso["conteudo"] = "\n".join(conteudo)

    print("\nNíveis disponíveis:")
    print("[1] Iniciante")
    print("[2] Intermediário")
    print("[3] Avançado")
    nivel_opcao = input(f"Escolha o nível do curso (atual: {curso['nivel']}, 1/2/3 ou Enter para manter): ").strip()

    niveis = {"1": "iniciante", "2": "intermediário", "3": "avançado"}
    if nivel_opcao:
        nivel = niveis.get(nivel_opcao)
        if nivel:
            cursos_nivel = [c for c in cursos if c["nivel"] == nivel and c != curso]
            if len(cursos_nivel) >= 7:
                print(f"Limite de 7 cursos para o nível '{nivel}' já atingido. Nível não alterado.")
            else:
                curso["nivel"] = nivel
        else:
            print("Nível inválido. Nível não alterado.")

    salvar_dados(CURSO_ARQUIVO, cursos)
    logger_admin.info(f"Curso editado: {curso['nome']} ({curso['nivel']})")
    print(f"Curso '{curso['nome']}' editado com sucesso.\n")


def excluir_curso():
    cursos = carregar_dados(CURSO_ARQUIVO)

    if not cursos:
        print("Nenhum curso cadastrado para excluir.")
        return

    print("\n=== Excluir Curso ===")
    for idx, curso in enumerate(cursos, 1):
        print(f"[{idx}] {curso['nome']} (Nível: {curso['nivel']})")
    print(f"[{len(cursos) + 1}] Cancelar")

    escolha = input("Escolha o curso que deseja excluir: ").strip()

    if escolha == str(len(cursos) + 1):
        print("Exclusão cancelada.")
        return

    if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(cursos):
        print("Opção inválida.")
        return

    idx_curso = int(escolha) - 1
    curso = cursos[idx_curso]

    confirmar = input(f"Tem certeza que deseja excluir o curso '{curso['nome']}'? (s/n): ").strip().lower()
    if confirmar == "s":
        cursos.pop(idx_curso)
        salvar_dados(CURSO_ARQUIVO, cursos)
        logger_admin.info(f"Curso excluído: {curso['nome']}")
        print(f"Curso '{curso['nome']}' excluído com sucesso.\n")
    else:
        print("Exclusão cancelada.")


def mostrar_estatisticas():

    print("\n=== Estatísticas do Sistema ===")
    print("[1] Estatísticas de Usuários")
    print("[2] Estatísticas de Acessos")
    print("[3] Estatísticas de Avaliações")
    print("[4] Voltar")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        gerar_estatisticas_usuarios()
    elif opcao == "2":
        gerar_estatisticas_acessos()
    elif opcao == "3":
        gerar_estatisticas_avaliacoes()
    elif opcao == "4":
        return
    else:
        print("Opção inválida!")


def menu_admin():
    if not autenticar_admin():
        return

    while True:
        print("=== MENU ADMIN ===")
        print("[1] Cadastrar curso")
        print("[2] Visualizar cursos")
        print("[3] Editar curso")
        print("[4] Excluir curso")
        print("[5] Ver estatísticas")
        print("[6] Logout")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_curso()
        elif opcao == "2":
            ver_cursos()
        elif opcao == "3":
            editar_curso()
        elif opcao == "4":
            excluir_curso()
        elif opcao == "5":
            mostrar_estatisticas()
        elif opcao == "6":
            confirmar = input("Tem certeza que deseja fazer logout? (s/n): ").strip().lower()
            if confirmar == "s":
                print("Logout realizado com sucesso.\n")
                logger_admin.info("Admin realizou logout.")
                break
        else:
            print("Opção inválida.\n")


if __name__ == "__main__":
    menu_admin()