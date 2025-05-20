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

LOG_ADMIN = "logs/logger_admin.log"

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
        print("===================================================")
        print(" ")
        print("============= LOGIN DE ADMINISTRADOR ==============")
        print(" ")
        print("===================================================")
        print("Digite 'voltar' a qualquer momento para retornar ao menu anterior.")

        usuario = input("Informe o usuário: ").strip()
        if usuario.lower() == "voltar":
            print("Retornando ao menu anterior...\n")
            return False 

        senha = getpass.getpass("Informe a senha: ").strip()
        if senha.lower() == "voltar":
            print("Retornando ao menu anterior...\n")
            return False

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

    print("===================================================")
    print(" ")
    print("============ MENU DE CADASTRO DE CURSO ============")
    print(" ")
    print("===================================================")
    print("[1] Iniciante")
    print("[2] Intermediário")
    print("[3] Avançado")
    print("[0] Voltar")
    print(" ")
    print("===================================================")

    nivel_opcao = input("Escolha o nível do curso (1/2/3 ou 0 para voltar): ").strip()

    if nivel_opcao == "0":
        print("Cadastro cancelado. Retornando ao menu anterior.")
        return

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

    print("Digite o conteúdo do curso (Digite 'salvar curso' em uma linha vazia para finalizar):")
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
        print("===================================================")
        print(" ")
        print("============= MENU DE NÍVEIS DE CURSO =============")
        print(" ")
        print("===================================================")
        print("[1] Cursos Iniciante")
        print("[2] Cursos Intermediário")
        print("[3] Cursos Avançado")
        print("[4] Voltar ao menu principal")
        print(" ")
        print("===================================================")
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
            print("===================================================")
            print(" ")
            print(f"========= CURSOS NÍVEL {nivel.upper()} =========")
            print(" ")
            print("===================================================")
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

    niveis = {"1": "iniciante", "2": "intermediário", "3": "avançado"}

    while True:
        print("===================================================")
        print(" ")
        print("============= MENU DE EDIÇÃO DE CURSO ============")
        print(" ")
        print("===================================================")
        print("[1] Editar curso Iniciante")
        print("[2] Editar curso Intermediário")
        print("[3] Editar curso Avançado")
        print("[0] Voltar")
        print(" ")
        print("===================================================")
        opcao_nivel = input("Escolha o nível dos cursos que deseja editar: ").strip()

        if opcao_nivel == "0":
            print("Retornando ao menu anterior.")
            return

        nivel_escolhido = niveis.get(opcao_nivel)
        if not nivel_escolhido:
            print("Opção inválida. Tente novamente.")
            continue

        cursos_nivel = [c for c in cursos if c["nivel"] == nivel_escolhido]
        if not cursos_nivel:
            print(f"Não há cursos cadastrados no nível '{nivel_escolhido}'.")
            continue

        while True:

            print("===================================================")
            print(" ")
            print(f"========= CURSOS NÍVEL {nivel_escolhido.capitalize()} =========")
            print(" ")
            print("===================================================")
            for idx, curso in enumerate(cursos_nivel, 1):
                print(f"[{idx}] {curso['nome']}")
            print("[0] Voltar")
            print(" ")
            print("===================================================")

            escolha = input("Escolha o curso que deseja editar (ou 0 para voltar): ").strip()

            if escolha == "0":
                break

            if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(cursos_nivel):
                print("Opção inválida. Tente novamente.")
                continue

            curso = cursos_nivel[int(escolha) - 1]

            print("===================================================")
            print(" ")
            print(f"======== EDITANDO CURSO '{curso['nome']}' ========")
            print(" ")
            print("===================================================")

            novo_nome = input(f"Novo nome (deixe vazio para manter '{curso['nome']}'): ").strip()
            if novo_nome:
                if any(c["nome"].lower() == novo_nome.lower() and c != curso for c in cursos):
                    print("Já existe um curso com esse nome. Edição cancelada.")
                    continue
                curso["nome"] = novo_nome

            print("Digite o novo conteúdo do curso (Digite 'salvar curso' em uma linha vazia para finalizar):")
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

            print("===================================================")
            print(" ")
            print("=========== ESCOLHA O NOVO NÍVEL DO CURSO =========")
            print(" ")
            print("===================================================")
            print("[1] Iniciante")
            print("[2] Intermediário")
            print("[3] Avançado")
            print("[0] Manter nível atual")
            print(" ")
            print("===================================================")

            nivel_opcao = input(f"Escolha o novo nível (atual: {curso['nivel']}): ").strip()
            if nivel_opcao == "0" or not nivel_opcao:
                print("Mantendo nível atual.")
            else:
                novo_nivel = niveis.get(nivel_opcao)
                if novo_nivel:
                    outros_cursos_nivel = [c for c in cursos if c["nivel"] == novo_nivel and c != curso]
                    if len(outros_cursos_nivel) >= 7:
                        print(f"Limite de 7 cursos para o nível '{novo_nivel}' já atingido. Nível não alterado.")
                    else:
                        curso["nivel"] = novo_nivel
                        print(f"Nível do curso alterado para '{novo_nivel}'.")
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

    print("===================================================")
    print(" ")
    print("============ MENU DE EXCLUSÃO DE CURSO ============")
    print(" ")
    print("===================================================")
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

    print("===================================================")
    print(" ")
    print("============== MENU DE ESTATÍSTICAS ===============")
    print(" ")
    print("===================================================")
    print("[1] Estatísticas de Usuários")
    print("[2] Estatísticas de Acessos")
    print("[3] Estatísticas de Avaliações")
    print("[4] Voltar")
    print(" ")
    print("===================================================")
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
        print("===================================================")
        print(" ")
        print("======== MENU DE ADMINISTRADOR AUTENTICADO ========")
        print(" ")
        print("===================================================")
        print("[1] Cadastrar curso")
        print("[2] Visualizar cursos")
        print("[3] Editar curso")
        print("[4] Excluir curso")
        print("[5] Ver estatísticas")
        print("[6] Logout")
        print(" ")
        print("===================================================")
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