import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from typing import Union, List, Dict, Any, cast

# url in docker-compose
SELENIUM_URL = "http://selenium-chrome:4444/wd/hub"

# waiting time
WAIT_TIME = 10

def read_spreadsheet(file_path: str) -> Union[List[Dict[str, Any]], None]:
  print(f"Lendo dados da planilha: {file_path}...")
  try:
    df = pd.read_excel(file_path, engine='openpyxl')

    # Convert spreadsheet data to dictionary list
    raw_data = df.to_dict('records')

    # tell pylance that we trust them
    data = cast(List[Dict[str, Any]], raw_data)

    print(f"Encontrados {len(data)} registros (rodadas) na planilha.")
    return data
  except FileNotFoundError:
    print(f"ERRO: Arquivo '{file_path}' não encontrado.")
    print("Por favor, baixe a planilha do site https://rpachallenge.com")
    print("Salve o arquivo na raiz do projeto como 'challenge.xlsx'")
    return None
  except Exception as error:
    print(f"Ocorreu um erro inesperado ao ler a planilha: {error}")
    return None

def start_driver() -> Union[webdriver.Remote, None]:
  print("Iniciando o driver do Selenium...")
  try:
    # config chrome
    chrome_options = Options()

    # configure browser with url
    driver = webdriver.Remote(
      command_executor=SELENIUM_URL,
      options=chrome_options,
    )

    print("Driver conectado com sucesso!")
    return driver
  except Exception as error:
    print(f"ERRO: Não foi possível conectar ao driver do Selenium em {SELENIUM_URL}")
    print(f"Detalhe do erro: {error}")
    print("Verifique se os contêineres estão rodando ('docker-compose up').")
    return None

def start_challenge(driver: webdriver.Remote) -> bool:
  print("Navegando até o site...")
  try:
    driver.get("https://rpachallenge.com")

    # wait creator
    wait = WebDriverWait(driver, WAIT_TIME)
    start_button = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//button[text()='Start']"))
    )

    start_button.click()

    print("Aguardando formulário da Rodada 1 carregar...")
    wait.until(EC.staleness_of(start_button))

    print("Desafio iniciado.")
    return True
  except (TimeoutException, WebDriverException) as error:
    print(f"ERRO: Não foi possível iniciar o desafio (botão 'Start').")
    print(f"Detalhe do erro: {error}")
    return False

def process_round(driver: webdriver.Remote, round_data: Dict[str, Any]) -> bool:
  print(f"Processando rodada com dados: {round_data['First Name']}...")
  try:
    # wait creator
    wait = WebDriverWait(driver, WAIT_TIME)

    # 1. add data to columns.
    for label_text, value_to_type in round_data.items():
      clean_label_text = label_text.strip()

      # 2. create sibling
      input_xpath = f"//label[normalize-space(text())='{clean_label_text}']/following-sibling::input"

      # 3. find the <input> by 'id' and fill it in
      input_element = wait.until(
        EC.visibility_of_element_located((By.XPATH, input_xpath))
      )
      input_element.send_keys(str(value_to_type))

    # 4. click on "Submit"
    submit_button = wait.until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
    )
    submit_button.click()

    print("Rodada enviada com sucesso.")
    return True
  except (TimeoutException, WebDriverException) as error:
    print(f"ERRO: Falha ao processar a rodada.")
    print(f"Detalhe do erro: {error}")
    print(f"Dados da rodada que falhou: {round_data}")
    return False
