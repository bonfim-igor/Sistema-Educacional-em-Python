import logging
from user.usuario import menu_usuario
from admins.admin import menu_admin

LOG_APP = "logs/logger_system.log"

logger_app = logging.getLogger('app')
logger_app.setLevel(logging.INFO)
file_handler_app = logging.FileHandler(LOG_APP)
file_handler_app.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger_app.addHandler(file_handler_app)

def main():
    logger_app.info("Início da execução do sistema.")
    while True:
        print("===================================================")
        print(" ")
        print("====== PLATAFORMA DE EDUCAÇÃO DIGITAL SEGURA ======")
        print(" ")
        print("===================================================")
        print("[1] Entrar como usuário")
        print("[2] Entrar como administrador")
        print("[3] Sair")
        print(" ")
        print("===================================================")
        opcao = input("Escolha uma opção entre (1-3): ").strip()

        if opcao not in {"1", "2", "3"}:
            print("Opção inválida.\n")
            continue

        if opcao == "1":
            logger_app.info("Usuário selecionou o menu de usuário.")
            menu_usuario()
        elif opcao == "2":
            logger_app.info("Usuário selecionou o menu de administrador.")
            menu_admin()
        elif opcao == "3":
            logger_app.info("Encerramento do sistema solicitado.")
            print("Encerrando sistema.")
            break

if __name__ == "__main__":
    main()