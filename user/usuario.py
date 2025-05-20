from datetime import datetime
import time
import shutil
import json
import os
import logging
import getpass
import bcrypt

USUARIO_ARQUIVO = "data/usuario.json"
CURSO_ARQUIVO = "data/cursos.json"
ACESSO_ARQUIVO = "data/acessos.json"
AVALIACOES_ARQUIVO = "data/avaliacoes.json"
BACKUP_PASTA = "data/backups"

LOG_USUARIO = "logs/logger_user.log"

logger_usuario = logging.getLogger('lusuario')
logger_usuario.setLevel(logging.INFO)
file_handler_usuario = logging.FileHandler(LOG_USUARIO)
file_handler_usuario.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger_usuario.addHandler(file_handler_usuario)

def hash_senha(senha: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verificar_senha(senha: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode('utf-8'), hashed.encode('utf-8'))
    except ValueError:
        return False

def carregar_dados(arquivo: str):
    if os.path.exists(arquivo):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            logger_usuario.warning(f"Falha ao carregar dados do arquivo {arquivo}.")
            return []
    return []

def salvar_dados(arquivo: str, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)

def criar_backup():
    if not os.path.exists(BACKUP_PASTA):
        os.makedirs(BACKUP_PASTA)

def backup_arquivo(origem: str):
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
    usuarios = carregar_dados(USUARIO_ARQUIVO)

    print("===================================================")
    print(" ")
    print("============== CADASTRO DE USUÁRIO ================")
    print(" ")
    print("===================================================")
    usuario = input("Informe o usuário (mínimo 3 caracteres, sem espaços (ou 'voltar' para sair): ").strip()
    if usuario.lower() == "voltar":
        print("Cadastro cancelado.\n")
        return
    if len(usuario) < 3 or " " in usuario:
        print("Usuário inválido. Tente novamente.\n")
        return

    if any(u["usuario"] == usuario for u in usuarios):
        print("Usuário já cadastrado.\n")
        return

    senha = getpass.getpass("Informe a senha (mínimo 6 caracteres (ou 'voltar' para sair): ").strip()
    if senha.lower() == "voltar":
        print("Cadastro cancelado.\n")
        return
    if len(senha) < 6:
        print("Senha muito curta.\n")
        return

    confirma = getpass.getpass("Confirme a senha: ").strip()
    if confirma.lower() == "voltar":
        print("Cadastro cancelado.\n")
        return
    if senha != confirma:
        print("Senhas não conferem.\n")
        return

    genero = input("Gênero (masculino/feminino (ou 'voltar' para sair): ").strip().lower()
    if genero == "voltar":
        print("Cadastro cancelado.\n")
        return
    if genero not in ["masculino", "feminino"]:
        print("Gênero inválido.\n")
        return

    idade_input = input("Informe sua idade (ou 'voltar' para sair): ").strip()
    if idade_input.lower() == "voltar":
        print("Cadastro cancelado.\n")
        return
    try:
        idade = int(idade_input)
        if idade <= 0:
            print("Idade inválida. A idade deve ser um número positivo.\n")
            return
    except ValueError:
        print("Idade inválida. Por favor, insira um número inteiro.\n")
        return

    novo = {
        "usuario": usuario,
        "senha": hash_senha(senha),
        "tipo": "usuario",
        "genero": genero,
        "idade": idade
    }

    usuarios.append(novo)
    salvar_dados(USUARIO_ARQUIVO, usuarios)
    logger_usuario.info(f"Usuário '{usuario}' cadastrado.")
    print("Cadastro realizado com sucesso.\n")

def autenticar_usuario():
    usuarios = carregar_dados(USUARIO_ARQUIVO)

    while True:
        print("===================================================")
        print(" ")
        print("================ LOGIN DE USUÁRIO =================")
        print(" ")
        print("===================================================")
        usuario = input("Informe o usuário (ou 'voltar' para sair): ").strip()
        if usuario.lower() == "voltar":
            print("Login cancelado.\n")
            return
        senha = getpass.getpass("Informe a senha (ou 'voltar' para sair): ").strip()
        if senha.lower() == "voltar":
            print("Login cancelado.\n")
            return

        user = next((u for u in usuarios if u["usuario"] == usuario), None)
        if user and verificar_senha(senha, user["senha"]):
            logger_usuario.info(f"Usuário '{usuario}' autenticado.")
            print(f"Bem-vindo, {usuario}!\n")
            menu_usuario_autenticado(user)
            return
        else:
            print("Credenciais inválidas.\n")

def ver_cursos(usuario):
    cursos = carregar_dados(CURSO_ARQUIVO)
    if not cursos:
        print("Nenhum curso disponível.\n")
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
            print("Opção inválida.\n")
            continue

        nivel = niveis[int(opcao) - 1]
        cursos_nivel = [c for c in cursos if c["nivel"] == nivel]

        if not cursos_nivel:
            print(f"Não há cursos cadastrados para o nível {nivel}.\n")
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

            if not escolha.isdigit() or not (1 <= int(escolha) <= len(cursos_nivel)):
                print("Opção inválida.\n")
                continue

            curso_selecionado = cursos_nivel[int(escolha) - 1]
            print(f"\nConteúdo do curso '{curso_selecionado['nome']}':")
            print(curso_selecionado['conteudo'])

            inicio_tempo = time.time()

            input("\nPressione Enter para voltar ao menu de cursos.")

            fim_tempo = time.time()
            tempo_acesso = round(fim_tempo - inicio_tempo, 2)

            acessos = carregar_dados(ACESSO_ARQUIVO)

            acesso_existente = next(
                (a for a in acessos if a["usuario"] == usuario["usuario"] and a["curso"] == curso_selecionado['nome']),
                None
            )

            if acesso_existente:
                acesso_existente["quantidade"] += 1
                acesso_existente["tempo"] += tempo_acesso
                acesso_existente["ultimo_acesso"] = datetime.now().isoformat()
            else:
                novo_acesso = {
                    "usuario": usuario["usuario"],
                    "curso": curso_selecionado['nome'],
                    "nivel": curso_selecionado['nivel'],
                    "quantidade": 1,
                    "tempo": tempo_acesso,
                    "primeiro_acesso": datetime.now().isoformat(),
                    "ultimo_acesso": datetime.now().isoformat()
                }
                acessos.append(novo_acesso)

            salvar_dados(ACESSO_ARQUIVO, acessos)

            print(f"Acesso registrado: {curso_selecionado['nome']}, duração {tempo_acesso} segundos.\n")

def avaliar_curso(usuario):
    cursos = carregar_dados(CURSO_ARQUIVO)
    if not cursos:
        print("Nenhum curso disponível para avaliação.\n")
        return

    niveis = ["iniciante", "intermediário", "avançado"]

    while True:
        print("===================================================")
        print(" ")
        print("==== SELECIONE O NÍVEL DO CURSO PARA AVALIAÇÃO ====")
        print(" ")
        print("===================================================")
        for i, nivel in enumerate(niveis, 1):
            print(f"[{i}] {nivel.capitalize()}")
        print(f"[{len(niveis)+1}] Voltar")

        escolha_nivel = input("Escolha o nível do curso para avaliar: ").strip()

        if escolha_nivel == str(len(niveis)+1):
            return

        if escolha_nivel not in [str(i) for i in range(1, len(niveis)+1)]:
            print("Opção inválida. Tente novamente.\n")
            continue

        nivel_escolhido = niveis[int(escolha_nivel) - 1]
        cursos_nivel = [c for c in cursos if c.get("nivel") == nivel_escolhido]

        if not cursos_nivel:
            print(f"Não há cursos cadastrados para o nível {nivel_escolhido}.\n")
            continue

        print("===================================================")
        print(" ")
        print(f"==== SELECIONE O CURSO DO NÍVEL {nivel_escolhido.capitalize()} =====")
        print(" ")
        print("===================================================")
        for i, curso in enumerate(cursos_nivel, 1):
            print(f"[{i}] {curso['nome']}")
        print(f"[{len(cursos_nivel)+1}] Voltar ao menu de níveis")

        escolha_curso = input("Escolha o número do curso que deseja avaliar: ").strip()

        if escolha_curso == str(len(cursos_nivel)+1):
            continue

        if not escolha_curso.isdigit() or not (1 <= int(escolha_curso) <= len(cursos_nivel)):
            print("Opção inválida. Tente novamente.\n")
            continue

        curso_escolhido = cursos_nivel[int(escolha_curso) - 1]
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
        return

def editar_dados(usuario):
    nome_antigo = usuario["usuario"]
    while True:
        print("===================================================")
        print(" ")
        print("============== MENU DE DADOS PESSOAIS =============")
        print(" ")
        print("===================================================")
        print("[1] Editar Nome")
        print("[2] Editar Senha")
        print("[3] Editar Idade")
        print("[4] Editar Gênero")
        print("[5] Excluir Conta")
        print("[6] Voltar")
        print(" ")
        print("===================================================")
        opcao = input("Escolha uma opção (1-6): ").strip()

        if opcao == "1":
            novo_nome = input("Digite o novo nome (ou pressione Enter para cancelar): ").strip()
            if not novo_nome:
                print("Edição de nome cancelada.")
                continue
            usuario["usuario"] = novo_nome

        elif opcao == "2":
            nova_senha = getpass.getpass("Digite a nova senha (ou pressione Enter para cancelar): ").strip()
            if not nova_senha:
                print("Edição de senha cancelada.")
                continue
            usuario["senha"] = hash_senha(nova_senha)

        elif opcao == "3":
            entrada = input("Digite a nova idade (ou pressione Enter para cancelar): ").strip()
            if not entrada:
                print("Edição de idade cancelada.")
                continue
            if not entrada.isdigit():
                print("Idade inválida.")
                continue
            nova_idade = int(entrada)
            usuario["idade"] = nova_idade

        elif opcao == "4":
            novo_genero = input("Digite o novo gênero (masculino/feminino (ou pressione Enter para cancelar): ").strip().lower()
            if not novo_genero:
                print("Edição de gênero cancelada.")
                continue
            usuario["genero"] = novo_genero

        elif opcao == "5":
            deletar_usuario(usuario)
            break

        elif opcao == "6":
            break

        else:
            print("Opção inválida.")
            continue

        usuarios = carregar_dados(USUARIO_ARQUIVO)
        for i, u in enumerate(usuarios):
            if u["usuario"] == nome_antigo:
                usuarios[i] = usuario
                salvar_dados(USUARIO_ARQUIVO, usuarios)
                print("Dados atualizados com sucesso!")
                break

def deletar_usuario(usuario):
    confirm = input(f"Tem certeza que deseja excluir a conta '{usuario['usuario']}'? (s/n): ").strip().lower()
    if confirm != "s":
        print("Exclusão cancelada.")
        return

    backup_arquivo(USUARIO_ARQUIVO)
    usuarios = carregar_dados(USUARIO_ARQUIVO)
    usuarios = [u for u in usuarios if u["usuario"] != usuario["usuario"]]
    salvar_dados(USUARIO_ARQUIVO, usuarios)
    logger_usuario.info(f"Usuário '{usuario['usuario']}' excluído.")
    print("Conta excluída com sucesso.")

def menu_usuario_autenticado(usuario):
    while True:
        print("===================================================")
        print(" ")
        print("=========== MENU DE USUARIO AUTENTICADO ===========")
        print(" ")
        print("===================================================")
        print("[1] Ver cursos")
        print("[2] Avaliar curso")
        print("[3] Editar dados pessoais")
        print("[4] Logout")
        print(" ")
        print("===================================================")
        opcao = input("Escolha uma opção entre (1-4): ").strip()

        if opcao == "1":
            ver_cursos(usuario)
        elif opcao == "2":
            avaliar_curso(usuario)
        elif opcao == "3":
            editar_dados(usuario)
            break
        elif opcao == "4":
            print("Logout realizado.\n")
            break
        else:
            print("Opção inválida.\n")

def menu_usuario():
    while True:
        print("===================================================")
        print(" ")
        print("========= MENU DE USUARIO NÃO AUTENTICADO =========")
        print(" ")
        print("===================================================")
        print("[1] Cadastrar")
        print("[2] Login")
        print("[3] Voltar")
        print(" ")
        print("===================================================")
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