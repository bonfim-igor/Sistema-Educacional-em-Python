import json
import hashlib
import os
import logging


USUARIO_ARQUIVO = "usuario.json"
CURSO_ARQUIVO = "cursos.json"
ACESSO_ARQUIVO = "acessos.json"
AVALIACOES_ARQUIVO = "avaliacoes.json"


ADMIN_USUARIO = "admin"
ADMIN_SENHA = "admin123"
ADMIN_SENHA_HASH = hashlib.sha256(ADMIN_SENHA.encode()).hexdigest()


LOG_ADMIN = "log_admin.log"

# Criação de um logger específico para o admin
logger_admin = logging.getLogger('admin')
logger_admin.setLevel(logging.INFO)
file_handler_admin = logging.FileHandler(LOG_ADMIN)
file_handler_admin.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger_admin.addHandler(file_handler_admin)


# Função que carrega dados de um arquivo JSON. Caso o arquivo não exista ou tenha erro no formato, retorna uma lista vazia
def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


# Função que salva dados em um arquivo JSON, substituindo o conteúdo anterior
def salvar_dados(arquivo, dados):
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)


# Função que autentica o administrador
# O loop continua até que o login seja bem-sucedido
def autenticar_admin():
    while True:
        # Solicita o nome de usuário e a senha do admin
        usuario = input("Informe o usuário: ")
        senha = input("Informe a senha: ")

        # Verifica se o nome de usuário e o hash da senha são iguais aos pré-definidos
        if usuario == ADMIN_USUARIO and hashlib.sha256(senha.encode()).hexdigest() == ADMIN_SENHA_HASH:
            print("Acesso concedido ao admin.\n")
            # Registra no log que o admin efetuou login com sucesso
            logger_admin.info(f"Admin '{usuario}' logado.")
            return  # Interrompe o loop ao logar com sucesso
        else:
            # Informa ao usuário que as credenciais estão incorretas
            print("Credenciais incorretas.\n")
            # Registra no log uma tentativa de login inválida
            logger_admin.warning("Tentativa de login admin inválida.")



def cadastrar_curso():
    # Carrega a lista de cursos já existentes a partir do arquivo JSON
    cursos = carregar_dados(CURSO_ARQUIVO)

    # Exibe as opções de níveis disponíveis
    print("\nNíveis disponíveis:")
    print("[1] Iniciante")
    print("[2] Intermediário")
    print("[3] Avançado")

    # Solicita que o usuário selecione o nível do curso
    nivel_opcao = input("Escolha o nível do curso (1/2/3): ").strip()

    # Mapeia a opção numérica para a string correspondente
    niveis = {"1": "iniciante", "2": "intermediário", "3": "avançado"}
    nivel = niveis.get(nivel_opcao)

    # Se a opção informada for inválida, cancela o cadastro do curso
    if not nivel:
        print("Nível inválido. Curso não cadastrado.")
        return

    # Verifica se já existem 5 cursos cadastrados para o nível escolhido
    cursos_nivel = [c for c in cursos if c["nivel"] == nivel]
    if len(cursos_nivel) >= 5:
        print(f"Limite de 5 cursos para o nível '{nivel}' já atingido.")
        return

    # Solicita ao usuário o nome do novo curso e remove espaços extras
    nome = input("Nome do curso: ").strip()

    # Verifica se já existe um curso com o mesmo nome (ignorando maiúsculas/minúsculas)
    if any(c["nome"].lower() == nome.lower() for c in cursos):
        print("Curso já cadastrado.")
        return

    # Solicita a descrição ou conteúdo do curso (texto grande)
    print("Digite o conteúdo do curso (Digite salvar curso em uma linha vazia para finalizar):")
    conteudo = []
    while True:
        linha = input()
        if linha == "salvar curso":
            break
        conteudo.append(linha)
    conteudo = "\n".join(conteudo)

    # Cria um dicionário com os dados do novo curso
    novo_curso = {
        "nome": nome,
        "conteudo": conteudo,
        "nivel": nivel
    }

    # Adiciona o novo curso à lista de cursos
    cursos.append(novo_curso)
    # Salva a lista atualizada de cursos no arquivo JSON
    salvar_dados(CURSO_ARQUIVO, cursos)
    # Registra no log do sistema que um novo curso foi cadastrado
    logger_admin.info(f"Curso cadastrado: {nome} ({nivel})")
    # Informa o usuário que o curso foi cadastrado com sucesso
    print(f"Curso '{nome}' cadastrado com sucesso no nível {nivel}.\n")


# Função que exibe os cursos cadastrados organizados por nível
def ver_cursos():
    # Carrega a lista de cursos a partir do arquivo JSON
    cursos = carregar_dados(CURSO_ARQUIVO)

    # Verifica se a lista de cursos está vazia
    if not cursos:
        print("Nenhum curso cadastrado.")
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

# Função que exibe estatísticas gerais do sistema
def ver_estatisticas():
    # Carrega a lista de acessos a cursos do arquivo ACESSO_ARQUIVO (acessos.json)
    acessos = carregar_dados(ACESSO_ARQUIVO)
    
    # Calcula o total de acessos, que é simplesmente o tamanho da lista de acessos
    total_acessos = len(acessos)

    # Carrega a lista de usuários do arquivo USUARIO_ARQUIVO (usuarios.json)
    usuarios = carregar_dados(USUARIO_ARQUIVO)
    
    # Inicializa um dicionário para contar os gêneros dos usuários
    generos = {"masculino": 0, "feminino": 0}
    
    # Itera sobre todos os usuários carregados para contar quantos são masculinos e femininos
    for u in usuarios:
        genero = u.get("genero")  # Obtém o gênero do usuário
        if genero in generos:  # Se o gênero for "masculino" ou "feminino"
            generos[genero] += 1  # Incrementa o contador correspondente ao gênero

    # Exibe as estatísticas gerais para o administrador
    print("\nEstatísticas:")
    print(f"- Total de acessos a cursos: {total_acessos}")  # Exibe o total de acessos
    print(f"- Usuários masculinos: {generos['masculino']}")  # Exibe o número de usuários masculinos
    print(f"- Usuários femininos: {generos['feminino']}")  # Exibe o número de usuários femininos

    # Registra no log do sistema que o administrador visualizou as estatísticas
    logger_admin.info("Admin visualizou estatísticas.")


# Função que exibe as avaliações dos cursos, incluindo a média das notas
def ver_avaliacoes():
    # Carrega os cursos e as avaliações a partir dos arquivos JSON correspondentes
    cursos = carregar_dados(CURSO_ARQUIVO)
    avaliacoes = carregar_dados(AVALIACOES_ARQUIVO)

    # Se não houver cursos cadastrados, exibe uma mensagem e encerra a função
    if not cursos:
        print("Nenhum curso cadastrado.")
        return

    # Exibe um título para as médias das avaliações
    print("\nMédia de avaliações por curso:")

    # Itera sobre cada curso carregado da lista de cursos
    for curso in cursos:
        # Filtra as notas das avaliações do curso atual
        notas = [a["nota"] for a in avaliacoes if a["curso"] == curso["nome"]]
        
        # Se houver avaliações para o curso, calcula a média
        if notas:
            media = sum(notas) / len(notas)  # Calcula a média das notas
            # Exibe o nome do curso, a média das avaliações e o número de avaliações feitas
            print(f"- {curso['nome']}: média {media:.2f} ({len(notas)} avaliações)")
        else:
            # Caso o curso não tenha avaliações, exibe uma mensagem indicando isso
            print(f"- {curso['nome']}: nenhuma avaliação")


# Função que exibe as avaliações dos cursos, agrupadas por nível
def ver_avaliacoes_por_nivel():
    # Carrega as avaliações a partir do arquivo JSON correspondente
    avaliacoes = carregar_dados(AVALIACOES_ARQUIVO)

    # Se não houver avaliações registradas, exibe uma mensagem e encerra a função
    if not avaliacoes:
        print("Nenhuma avaliação registrada.")
        return

    # Define os níveis dos cursos que serão considerados: iniciante, intermediário, e avançado
    niveis = ["iniciante", "intermediário", "avançado"]

    # Exibe um título para as médias das avaliações por nível
    print("\nMédia de avaliações por nível de curso:")

    # Itera sobre cada nível definido na lista 'niveis'
    for nivel in niveis:
        # Filtra as notas das avaliações que correspondem ao nível atual
        notas = [a["nota"] for a in avaliacoes if a.get("nivel") == nivel]
        
        # Se houver avaliações para o nível, calcula a média das notas
        if notas:
            media = sum(notas) / len(notas)  # Calcula a média das notas
            # Exibe o nível (com a primeira letra maiúscula), a média das avaliações e o número de avaliações feitas
            print(f"- {nivel.capitalize()}: média {media:.2f} ({len(notas)} avaliações)")
        else:
            # Caso o nível não tenha avaliações, exibe uma mensagem indicando isso
            print(f"- {nivel.capitalize()}: nenhuma avaliação.")


# Função que exibe o menu do administrador após autenticação
def menu_admin():
    autenticar_admin()

    while True:
        print("=== MENU ADMIN ===")
        print("[1] Cadastrar curso")
        print("[2] Ver cursos")
        print("[3] Ver estatísticas de usuários")
        print("[4] Ver avaliações dos cursos")
        print("[5] Ver avaliações por nível")
        print("[6] Logout")
        opcao = input("Escolha uma opção entre (1-6): ")

        if opcao == "1":
            cadastrar_curso()
        elif opcao == "2":
            ver_cursos()
        elif opcao == "3":
            ver_estatisticas()
        elif opcao == "4":
            ver_avaliacoes()
        elif opcao == "5":
            ver_avaliacoes_por_nivel()
        elif opcao == "6":
            print("Logout realizado.\n")
            break
        else:
            print("Opção inválida.\n")