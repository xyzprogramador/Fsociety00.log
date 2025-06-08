def Cnpj(requests, cian, white, colorama):
    import re
    from time import sleep

    print(f"\n{cian}Digite o CNPJ:{white}", end='')
    cnpj = input().strip()

    # Validação simples
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    if len(cnpj) != 14:
        print(f"{colorama.Fore.RED}CNPJ inválido. Deve conter 14 dígitos.{white}")
        return

    url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
    print(f"{cian}Consultando CNPJ...{white}")
    sleep(1)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"\n{colorama.Fore.GREEN}Resultado da Consulta:{white}")
            print(f"Razão Social: {data.get('nome')}")
            print(f"Fantasia: {data.get('fantasia')}")
            print(f"Situação: {data.get('situacao')}")
            print(f"Data de Abertura: {data.get('abertura')}")
            print(f"UF: {data.get('uf')} | Município: {data.get('municipio')}")
        else:
            print(f"{colorama.Fore.RED}Erro na consulta. Código: {response.status_code}{white}")
    except Exception as e:
        print(f"{colorama.Fore.RED}Erro ao consultar o CNPJ: {e}{white}")
