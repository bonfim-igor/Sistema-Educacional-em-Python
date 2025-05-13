from usuario import menu_usuario
from admin import menu_admin


# Função principal que exibe o menu inicial do sistema
def main():
    while True:
        print("=== MENU PRINCIPAL ===")
        print("[1] Entrar como usuário")
        print("[2] Entrar como administrador")
        print("[3] Sair")
        opcao = input("Escolha entre (1-3): ")

        if opcao == "1":
            menu_usuario()
        elif opcao == "2":
            menu_admin()
        elif opcao == "3":
            print("Encerrando sistema.")
            break
        else:
            print("Opção inválida.\n")

if __name__ == "__main__":
    main()