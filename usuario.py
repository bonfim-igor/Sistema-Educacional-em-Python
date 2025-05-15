from datetime import datetime
import shutil
import json
import hashlib
import os
import logging


USUARIO_ARQUIVO = "usuario.json"
CURSO_ARQUIVO = "cursos.json"
ACESSO_ARQUIVO = "acessos.json"
AVALIACOES_ARQUIVO = "avaliacoes.json"


LOG_USUARIO = "log_usuario.log"

# Criação de um logger específico para o usuário
logger_usuario = logging.getLogger('usuario')
logger_usuario.setLevel(logging.INFO)
file_handler_usuario = logging.FileHandler(LOG_USUARIO)
file_handler_usuario.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger_usuario.addHandler(file_handler_usuario)


# Gera o hash SHA-256 da senha para armazenar com segurança
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


# Carrega os dados de um arquivo JSON, retornando uma lista vazia se o arquivo não existir
def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


# Salva os dados no arquivo JSON, formatando com indentação
def salvar_dados(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)


# Função que permite o cadastro de um novo usuário
def cadastrar_usuario():
    # Carrega a lista de usuários existentes a partir do arquivo JSON
    usuarios = carregar_dados(USUARIO_ARQUIVO)
    # Solicita ao usuário o nome de usuário que deseja cadastrar
    usuario = input("Informe o usuário: ")
    # Solicita ao usuário a senha desejada para o cadastro
    senha = input("Informe a senha: ")

    # Verifica se o nome de usuário já está cadastrado no sistema
    for u in usuarios:
        if u["usuario"] == usuario:
            print("Usuário já cadastrado.")  # Informa que o nome de usuário já existe
            return  # Interrompe a função, pois o cadastro não pode continuar

    # Solicita o gênero do usuário e o normaliza para minúsculo
    genero = input("Gênero (masculino/feminino): ").strip().lower()
    # Verifica se o gênero informado é válido
    if genero not in ["masculino", "feminino"]:
        print("Gênero inválido.")  # Informa que o gênero fornecido é inválido
        return  # Interrompe a função, pois o cadastro não pode continuar

    # Cria um novo dicionário com os dados do novo usuário
    novo = {
        "usuario": usuario,
        "senha": hash_senha(senha),  # Aplica a função de hash à senha para segurança
        "tipo": "usuario",  # Define o tipo como 'usuario' para esse novo cadastro
        "genero": genero  # Armazena o gênero do usuário
    }

    # Adiciona o novo usuário à lista de usuários
    usuarios.append(novo)
    # Salva a lista atualizada de usuários no arquivo JSON
    salvar_dados(USUARIO_ARQUIVO, usuarios)
    # Registra no log do sistema que um novo usuário foi cadastrado
    logger_usuario.info(f"Usuário '{usuario}' cadastrado.")
    # Informa o sucesso do cadastro
    print("Cadastro realizado com sucesso.\n")


# Função que autentica um usuário no sistema
def autenticar_usuario():
    # Carrega a lista de usuários cadastrados a partir do arquivo JSON
    usuarios = carregar_dados(USUARIO_ARQUIVO)

    # Loop contínuo até que o usuário forneça credenciais válidas
    while True:
        # Solicita ao usuário que informe seu nome de usuário e senha
        usuario = input("Informe o usuário: ")
        senha = input("Informe a senha: ")
        
        # Aplica uma função de hash à senha fornecida para garantir que seja comparada de forma segura
        senha_hash = hash_senha(senha)

        # Itera sobre todos os usuários cadastrados
        for u in usuarios:
            # Verifica se o nome de usuário e a senha correspondem a um usuário válido
            if u["usuario"] == usuario and u["senha"] == senha_hash:
                # Caso as credenciais sejam válidas, registra no log a autenticação
                logger_usuario.info(f"Usuário '{usuario}' autenticado.")
                
                # Exibe uma mensagem de boas-vindas ao usuário autenticado
                print(f"Bem-vindo, {usuario}!\n")
                
                # Chama o menu de opções para o usuário autenticado
                menu_usuario_autenticado(u)
                
                # Retorna para sair da função após a autenticação bem-sucedida
                return
        
        # Se as credenciais não corresponderem, exibe uma mensagem de erro e solicita novamente
        print("Credenciais inválidas.\n")


# Função que permite ao usuário visualizar os cursos disponíveis e registra o acesso do usuário
def ver_cursos(usuario):
    # Carrega a lista de cursos disponíveis a partir do arquivo JSON
    cursos = carregar_dados(CURSO_ARQUIVO)

    # Verifica se a lista de cursos está vazia
    if not cursos:
        print("Nenhum curso disponível.")
        return

    # Mapeia os níveis de cursos para facilitar a navegação
    niveis = ["iniciante", "intermediário", "avançado"]

    while True:
        print("\n=== MENU DE CURSOS ===")
        print("[1] Cursos Iniciante")
        print("[2] Cursos Intermediário")
        print("[3] Cursos Avançado")
        print("[4] Voltar ao menu principal")
        opcao = input("Escolha uma opção entre (1-4): ").strip()

        # Verifica se a opção é para voltar ao menu principal
        if opcao == "4":
            break

        # Valida a escolha do nível
        if opcao not in ["1", "2", "3"]:
            print("Opção inválida.")
            continue

        # Seleciona o nível correspondente
        nivel = niveis[int(opcao) - 1]
        # Filtra os cursos pelo nível selecionado
        cursos_nivel = [c for c in cursos if c["nivel"] == nivel]

        # Verifica se há cursos cadastrados para o nível selecionado
        if not cursos_nivel:
            print(f"Não há cursos cadastrados para o nível {nivel}.")
            continue

        while True:
            print(f"\n=== CURSOS NÍVEL {nivel.upper()} ===")
            for idx, curso in enumerate(cursos_nivel, 1):
                print(f"[{idx}] {curso['nome']}")
            print(f"[{len(cursos_nivel) + 1}] Voltar")

            escolha = input("Escolha um curso para ver o conteúdo: ").strip()

            # Verifica se a escolha é para voltar
            if escolha == str(len(cursos_nivel) + 1):
                break

            # Verifica se a escolha está dentro do intervalo válido
            if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(cursos_nivel):
                print("Opção inválida.")
                continue

            # Mostra o conteúdo do curso escolhido
            curso_selecionado = cursos_nivel[int(escolha) - 1]
            print(f"\nConteúdo do curso '{curso_selecionado['nome']}':")
            print(curso_selecionado['conteudo'])
            input("\nPressione Enter para voltar ao menu de cursos.")

    # Carrega a lista de acessos ao arquivo JSON
    acessos = carregar_dados(ACESSO_ARQUIVO)

    # Registra o acesso do usuário, incluindo seu nome de usuário e o número de cursos disponíveis
    acessos.append({"usuario": usuario["usuario"], "curso_count": len(cursos)})

    # Salva a lista de acessos atualizada no arquivo de acessos
    salvar_dados(ACESSO_ARQUIVO, acessos)


# Função que permite que o usuário avalie um curso
def avaliar_curso(usuario):
    # Carrega os cursos disponíveis a partir do arquivo JSON
    cursos = carregar_dados(CURSO_ARQUIVO)

    # Se não houver cursos disponíveis, exibe uma mensagem e retorna
    if not cursos:
        print("Nenhum curso disponível para avaliação.")
        return

    # Exibe a lista de cursos disponíveis para avaliação, numerados
    print("\nCursos disponíveis para avaliação:")
    for i, curso in enumerate(cursos):
        print(f"[{i+1}] {curso['nome']}")

    try:
        # Solicita ao usuário que escolha um curso para avaliar, verificando se a entrada é válida
        escolha = int(input("Escolha o número do curso que deseja avaliar: "))
        # Verifica se o número informado está dentro do intervalo de cursos disponíveis
        if escolha < 1 or escolha > len(cursos):
            print("Curso inválido.")
            return
    except ValueError:
        # Caso o usuário não insira um número válido, exibe mensagem de erro
        print("Entrada inválida.")
        return

    # Armazena as informações do curso escolhido
    curso_escolhido = cursos[escolha - 1]
    nome_curso = curso_escolhido["nome"]
    nivel_curso = curso_escolhido.get("nivel", "não especificado")

    # Carrega as avaliações existentes a partir do arquivo JSON
    avaliacoes = carregar_dados(AVALIACOES_ARQUIVO)

    # Verifica se o usuário já avaliou o curso escolhido
    for avaliacao in avaliacoes:
        if avaliacao["usuario"] == usuario["usuario"] and avaliacao["curso"] == nome_curso:
            print("Você já avaliou este curso.")
            return

    try:
        # Solicita que o usuário forneça uma nota para o curso, de 1 a 5
        nota = int(input("Avalie de 1 a 5: "))
        # Verifica se a nota fornecida está dentro do intervalo permitido
        if nota < 1 or nota > 5:
            print("Nota fora do intervalo.")
            return
    except ValueError:
        # Caso o usuário insira algo que não seja um número, exibe uma mensagem de erro
        print("Nota inválida.")
        return

    # Adiciona a avaliação do usuário ao conjunto de avaliações
    avaliacoes.append({
        "usuario": usuario["usuario"],
        "curso": nome_curso,
        "nivel": nivel_curso,
        "nota": nota
    })

    # Salva a lista de avaliações atualizada no arquivo JSON
    salvar_dados(AVALIACOES_ARQUIVO, avaliacoes)
    
    # Informa ao usuário que a avaliação foi registrada com sucesso
    print("Avaliação registrada com sucesso.")


# Função que permite excluir a conta de um usuário
def deletar_usuario(usuario):
    # Solicita confirmação do administrador antes de excluir a conta do usuário
    confirm = input(f"Tem certeza que deseja excluir a conta '{usuario['usuario']}'? (s/n): ").strip().lower()
    
    # Se a resposta não for "s" (sim), a exclusão é cancelada
    if confirm != "s":
        print("Exclusão cancelada.\n")
        return

    # Gera um nome de backup para o arquivo de usuários, incluindo a data e hora atuais para evitar sobreposição
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_backup = f"backup_usuario_{usuario['usuario']}_{data_hora}.json"
    
    try:
        # Tenta copiar o arquivo de usuários atual para o arquivo de backup
        shutil.copy("usuario.json", nome_backup)
        # Informa ao usuário que o backup foi criado com sucesso
        print(f"Backup salvo como '{nome_backup}'")
        # Registra no log que o backup foi criado antes da exclusão do usuário
        logger_usuario.info(f"Backup criado antes da exclusão do usuário '{usuario['usuario']}'.")
    except Exception as e:
        # Se ocorrer um erro ao criar o backup, exibe uma mensagem de erro e registra no log
        print(f"Erro ao criar backup: {e}")
        logger_usuario.error(f"Erro ao criar backup: {e}")

    # Carrega a lista de usuários do arquivo JSON
    usuarios = carregar_dados(USUARIO_ARQUIVO)
    # Filtra a lista de usuários para remover o usuário que está sendo excluído
    usuarios = [u for u in usuarios if u["usuario"] != usuario["usuario"]]
    
    # Salva a lista de usuários atualizada de volta no arquivo JSON
    salvar_dados(USUARIO_ARQUIVO, usuarios)
    # Registra no log que o usuário foi excluído
    logger_usuario.info(f"Usuário '{usuario['usuario']}' excluído.")
    
    # Informa ao administrador que a conta foi excluída com sucesso
    print("Conta excluída com sucesso.\n")


# Menu para usuários autenticados
def menu_usuario_autenticado(usuario):
    while True:
        print("=== MENU USUÁRIO ===")
        print("[1] Ver cursos")
        print("[2] Avaliar curso")
        print("[3] Excluir minha conta")
        print("[4] Logout")
        opcao = input("Escolha uma opção entre (1-4): ")

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


# Menu inicial para usuários não autenticados
def menu_usuario():
    while True:
        print("=== MENU INICIAL ===")
        print("[1] Cadastrar")
        print("[2] Login")
        print("[3] Voltar")
        opcao = input("Escolha entre (1-3): ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            autenticar_usuario()
        elif opcao == "3":
            break
        else:
            print("Opção inválida.\n")