import json
import statistics
import matplotlib.pyplot as plt

def carregar_dados(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def calcular_media(valores):
    return statistics.mean(valores) if valores else 0

def calcular_moda(valores):
    try:
        return statistics.mode(valores)
    except statistics.StatisticsError:
        return 'Sem moda'

def calcular_mediana(valores):
    return statistics.median(valores) if valores else 0

def gerar_grafico(valores, titulo, xlabel):
    plt.figure(figsize=(8, 5))
    plt.hist(valores, bins=10, color='skyblue', edgecolor='black')
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel('Frequência')
    plt.show()

def gerar_estatisticas_usuarios():
    usuarios = carregar_dados('data/usuario.json')
    idades = [user['idade'] for user in usuarios if 'idade' in user]
    generos = [user['genero'] for user in usuarios if 'genero' in user]

    while True:
        print("\n=== Menu Estatísticas Usuário")
        print("[1] Estatísticas de Idade")
        print("[2] Estatísticas de Gênero")
        print("[3] Voltar")

        escolha = input("Escolha uma opção entre (1-3): ").strip()

        if escolha == '1':
            if not idades:
                print("Não há estatísticas de idades para exibir.")
            else:
                media_idade = calcular_media(idades)
                moda_idade = calcular_moda(idades)
                mediana_idade = calcular_mediana(idades)
                print(f'Média das idades: {media_idade}')
                print(f'Moda das idades: {moda_idade}')
                print(f'Mediana das idades: {mediana_idade}')
                gerar_grafico(idades, 'Distribuição de Idades', 'Idade')

        elif escolha == '2':
            if not generos:
                print("Não há estatísticas de gênero para exibir.")
            else:
                from collections import Counter
                contagem_generos = Counter(generos)
                print("Contagem de gêneros:")
                for genero, quantidade in contagem_generos.items():
                 print(f"  {genero.capitalize()}: {quantidade}")

                plt.figure(figsize=(6,4))
                plt.bar(contagem_generos.keys(), contagem_generos.values(), color='lightgreen', edgecolor='black')
                plt.title('Distribuição de Gênero')
                plt.xlabel('Gênero')
                plt.ylabel('Quantidade')
                plt.show()

        elif escolha == '3':
            print("Saindo das estatísticas de usuários.")
            break
        else:
            print("Opção inválida, tente novamente.")

def gerar_estatisticas_acessos():
    acessos = carregar_dados('data/acessos.json')
    num_acessos = [acesso['quantidade'] for acesso in acessos if 'quantidade' in acesso]
    tempos = [acesso['tempo'] for acesso in acessos if 'tempo' in acesso]

    if not num_acessos and not tempos:
        print("Não há estatísticas de acessos para exibir.")
        return

    while True:
        print("\n=== Estatísticas de Acessos ===")
        print("[1] Estatísticas de Número de Acessos")
        print("[2] Estatísticas de Tempo de Acesso")
        print("[3] Voltar")
        escolha = input("Escolha uma opção entre (1-3): ").strip()

        if escolha == '1':
            if not num_acessos:
                print("Não há dados de número de acessos para exibir.")
            else:
                media_acessos = calcular_media(num_acessos)
                moda_acessos = calcular_moda(num_acessos)
                mediana_acessos = calcular_mediana(num_acessos)
                print(f'Média de acessos: {media_acessos}')
                print(f'Moda de acessos: {moda_acessos}')
                print(f'Mediana de acessos: {mediana_acessos}')
                gerar_grafico(num_acessos, 'Número de Acessos', 'Quantidade')

        elif escolha == '2':
            if not tempos:
                print("Não há dados de tempo de acesso para exibir.")
            else:
                media_tempo = calcular_media(tempos)
                moda_tempo = calcular_moda(tempos)
                mediana_tempo = calcular_mediana(tempos)
                print(f'Média do tempo de acesso: {media_tempo}')
                print(f'Moda do tempo de acesso: {moda_tempo}')
                print(f'Mediana do tempo de acesso: {mediana_tempo}')
                gerar_grafico(tempos, 'Tempo Médio de Uso', 'Tempo (minutos)')

        elif escolha == '3':
            print("Saindo das estatísticas de acessos.")
            break
        else:
            print("Opção inválida, tente novamente.")

def gerar_estatisticas_avaliacoes():
    avaliacoes = carregar_dados('data/avaliacoes.json')
    if not avaliacoes:
        print("Não há avaliações para exibir estatísticas.")
        return

    # Agrupar avaliações por curso
    avaliacoes_por_curso = {}
    for av in avaliacoes:
        curso = av.get("curso", "Desconhecido")
        nota = av.get("nota")
        if nota is not None:
            avaliacoes_por_curso.setdefault(curso, []).append(nota)

    if not avaliacoes_por_curso:
        print("Nenhuma avaliação válida encontrada.")
        return

    print("=== Estatísticas de Avaliações por Curso ===")
    medias = []
    cursos = []
    for curso, notas in avaliacoes_por_curso.items():
        media = statistics.mean(notas)
        maxima = max(notas)
        minima = min(notas)
        quantidade = len(notas)
        cursos.append(curso)
        medias.append(media)
        print(f"Curso: {curso}")
        print(f"  Quantidade de avaliações: {quantidade}")
        print(f"  Média das notas: {media:.2f}")
        print(f"  Nota máxima: {maxima}")
        print(f"  Nota mínima: {minima}\n")

    plt.figure(figsize=(10,6))
    plt.bar(cursos, medias, color='lightblue', edgecolor='black')
    plt.title('Média das Notas por Curso')
    plt.xlabel('Curso')
    plt.ylabel('Média das Notas')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()