import os
import colorama
import time
import requests
import re # Import regex for better input validation
from assets.searchCnpj import Cnpj # Import the Cnpj function
from assets.cpf import menu
# Initialize Colorama for cross-platform colored output
colorama.just_fix_windows_console()

# --- Global Color Definitions (Moved for better organization) ---


# --- API Endpoints (Centralized for easy modification) ---
# Your original API_ENDPOINTS was commented out or missing.
# If you need specific APIs for CPF, add them here.
# For CNPJ, searchCnpj.py uses 'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
API_ENDPOINTS = {
    "CPF": "https://api.cpf.com/v1/cpf/{cpf}" # Example, replace with your actual CPF API
}
Colors = colorama.Fore

# --- Banner ---
BANNER = f"""{Colors.RED}
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄   ▄▄▄▄▄▄▄▄▄    ▄▄▄▄▄▄▄▄▄     ▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌ ▐░░░░░░░░░▌  ▐░░░░░░░░░▌   ▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ ▐░▌       ▐░▌▐░█░█▀▀▀▀▀█░▌▐░█░█▀▀▀▀▀█░▌  ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ 
▐░▌          ▐░▌          ▐░▌       ▐░▌▐░▌               ▐░▌     ▐░▌               ▐░▌     ▐░▌       ▐░▌▐░▌▐░▌    ▐░▌▐░▌▐░▌    ▐░▌  ▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     ▐░▌          
▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░▌               ▐░▌     ▐░█▄▄▄▄▄▄▄▄▄      ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▐░▌   ▐░▌▐░▌ ▐░▌   ▐░▌  ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌     ▐░▌     ▐░█▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌               ▐░▌     ▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌▐░▌  ▐░▌  ▐░▌  ▐░▌       ▐░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░▌               ▐░▌     ▐░█▀▀▀▀▀▀▀▀▀      ▐░▌      ▀▀▀▀█░█▀▀▀▀ ▐░▌   ▐░▌ ▐░▌▐░▌   ▐░▌ ▐░▌  ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌     ▐░▌     ▐░█▀▀▀▀▀▀▀▀▀ 
▐░▌                    ▐░▌▐░▌       ▐░▌▐░▌               ▐░▌     ▐░▌               ▐░▌          ▐░▌     ▐░▌    ▐░▌▐░▌▐░▌    ▐░▌▐░▌  ▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     ▐░▌          
▐░▌           ▄▄▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄  ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄      ▐░▌          ▐░▌     ▐░█▄▄▄▄▄█░█░▌▐░█▄▄▄▄▄█░█░▌▄ ▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌     ▐░▌     ▐░█▄▄▄▄▄▄▄▄▄ 
▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌          ▐░▌      ▐░░░░░░░░░▌  ▐░░░░░░░░░▌▐░▌▐░░░░░░░░░░▌ ▐░▌       ▐░▌     ▐░▌     ▐░░░░░░░░░░░▌
 ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀            ▀        ▀▀▀▀▀▀▀▀▀    ▀▀▀▀▀▀▀▀▀  ▀  ▀▀▀▀▀▀▀▀▀▀   ▀         ▀       ▀       ▀▀▀▀▀▀▀▀▀▀▀ 
{Colors.RESET}
"""

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Displays the application banner."""
    clear_screen()
    print(BANNER)
    print(f'{Colors.GREEN}>(CARREGANDO, OBRIGADO POR USAR){Colors.RESET}')
    time.sleep(1) # Reduced sleep time for faster startup

def validate_cpf(cpf_str):
    """
    Validates a Brazilian CPF number.
    Checks for length (11 digits) and if it's numeric.
    For a full, mathematically correct CPF validation, a more complex algorithm is needed.
    """
    if not isinstance(cpf_str, str):
        return False
    cpf_str = re.sub(r'[^0-9]', '', cpf_str) # Remove non-digits
    return len(cpf_str) == 11 and cpf_str.isdigit()


  
def main_menu():
    """Displays the main menu and handles user choices."""
    while True:
        clear_screen()
        print(BANNER)
        print(f'\n{Colors.BLUE}######### {Colors.WHITE}MENU PRINCIPAL{Colors.BLUE} #########{Colors.RESET}')
        print(f'{Colors.GREEN}1. {Colors.WHITE}Consultar CPF{Colors.RESET}')
        print(f'{Colors.GREEN}2. {Colors.WHITE}Consultar CNPJ{Colors.RESET}')
        print(f'{Colors.RED}3. {Colors.WHITE}Sair{Colors.RESET}')
        print(f'{Colors.BLUE}################################{Colors.RESET}')

        choice = input(f'\n{Colors.YELLOW}Escolha uma opção: {Colors.RESET}').strip()

        if choice == '1':
            os.system('cls' if os.name=='nt' else 'clear')
            menu()
        elif choice == '2':
            clear_screen()
            print(f'\n{Colors.BLUE}########## #################### ##########')
            print(f'{Colors.BLUE}########## ### Consulta CNPJ ### ##########')
            print(f'{Colors.BLUE}########## #################### ##########{Colors.RESET}')
            Cnpj(requests=requests,cian=colorama.Fore.CYAN, white=colorama.Fore.RESET,colorama=colorama)
            input(f'\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.RESET}') # Keep this for consistent flow
        elif choice == '3':
            print(f'{Colors.GREEN}Saindo... Obrigado por usar!{Colors.RESET}')
            break
        else:
            print(f'{Colors.RED}Opção inválida. Por favor, escolha 1, 2 ou 3.{Colors.RESET}')
            time.sleep(1) # Small delay before clearing and showing menu again

if __name__ == "__main__":
    display_banner() # Initial banner display
    main_menu() # Start the main menu loop