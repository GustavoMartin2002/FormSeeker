import time
from functions.automation_core import (
    read_spreadsheet,
    start_driver,
    start_challenge,
    process_round,
)

# const for spreadsheet name
EXCEL_FILE = "challenge.xlsx"

def main():
    print("--- 🤖 Iniciando BOT ---")

    # 1. read data spreadsheet
    spreadsheet_data = read_spreadsheet(file_path=EXCEL_FILE)
    if not spreadsheet_data:
        print("Erro na leitura da planilha...")
        print("Encerrando bot.")
        return

    # 2. driver init (browser)
    driver = start_driver()
    if not driver:
        print("Erro na inicialização do driver...")
        print("Encerrando bot.")
        return

    # UX: loading
    print("Pré-carregando o site para visualização...")
    try:
        driver.get("https://rpachallenge.com")
    except Exception as error:
        print(f"Aviso: Erro ao pré-carregar site: {error}")

    print("\n----------------------------------------------------")
    print("⚡ O NAVEGADOR JÁ ESTÁ ABERTO!")
    print("A AUTOMAÇÃO COMEÇARÁ EM 10 SEGUNDOS...")
    print("Acesse http://localhost:7900 AGORA.")
    print("----------------------------------------------------\n")

    for i in range(10, 0, -1):
        print(f"Iniciando em {i} segundos...", flush=True)
        time.sleep(1)

    # 3. exec challenger
    try:
        # 3.1 click start
        if not start_challenge(driver):
            print("Falha ao iniciar o desafio...")
            print("Encerrando bot.")
            return

        # 3.2 main Loop
        for i, line_data in enumerate(spreadsheet_data, start=1):
            print(f"\n--- Processando Rodada {i} de {len(spreadsheet_data)} ---")

            # round function
            round_successful = process_round(driver, line_data)
            if not round_successful:
                print(f"ERRO CRÍTICO: Robô interrompido na rodada {i}.")
                return

            time.sleep(0.5)

        # 3.3 success
        print("\n--- ✅ SUCESSO! ---")
        print("Todas rodadas foram completadas.")
        print("Exibindo resultados por 10 segundos...")
        time.sleep(10)
    except Exception as error:
        print(f"ERRO INESPERADO durante a execução: {error}")
    # 4. cleaning
    finally:
        print("Fechando o navegador e encerrando a sessão do Selenium...")
        driver.quit()
        print("--- 🤖 Finalizando BOT ---")

if __name__ == "__main__":
    main()
