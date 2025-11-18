import pytest
from functions.automation_core import (
  read_spreadsheet,
  start_driver,
  start_challenge,
  process_round,
)
from selenium.webdriver.remote.webdriver import WebDriver

# file name
TEST_FILE = "challenge.xlsx"

# READ_SPREADSHEET
def test_read_spreadsheet_success():
  print("[Teste] Lendo planilha real...")
  data = read_spreadsheet(TEST_FILE)

  assert data is not None, "Falha:🟥 A função retornou None para um arquivo existente."
  assert len(data) == 10, f"Falha:🟥 Esperava 10 registros, obteve {len(data)}."
  assert isinstance(data[0], dict), "Falha:🟥 O registro não é um dicionário."

  # column verification
  assert "First Name" in data[0]
  assert "Last Name " in data[0] # check column spacing
  print("-> Leitura da planilha:🟩 SUCESSO")

def test_read_spreadsheet_file_not_found():
  print("[Teste] Testando arquivo inexistente...")
  data = read_spreadsheet("arquivo_fantasma.xlsx")
  assert data is None, "Falha:🟥 Deveria retornar None para arquivo inexistente."
  print("-> Tratamento de erro de arquivo:🟩 SUCESSO")

# START_DRIVER
@pytest.fixture(scope="module")
def driver_setup():
  print("[Fixture] Iniciando Driver para testes...")
  driver = start_driver()
  if not driver:
    pytest.fail("🟥 Não foi possível iniciar o driver para os testes.")
  yield driver
  print("[Fixture] Fechando Driver...")
  driver.quit()

def test_start_driver_function(driver_setup):
  assert driver_setup is not None
  assert isinstance(driver_setup, WebDriver)
  print("-> Inicialização do Driver:🟩 SUCESSO")

# START_CHALLENGE
def test_start_challenge(driver_setup):
  print("[Teste] Iniciando desafio (clicando em Start)...")
  success = start_challenge(driver_setup)

  assert success is True, "🟥 Falha ao iniciar o desafio."
  assert "rpa challenge" in driver_setup.title.lower(), f"🟥 Título incorreto: {driver_setup.title}"
  print("-> Botão Start e Carregamento:🟩 SUCESSO")

# PROCESS_ROUND
def test_process_round(driver_setup):
  print("[Teste] Processando uma rodada de teste...")

  # spreadsheet data simulation
  dummy_data = {
    "First Name": "Robot",
    "Last Name ": "Tester", # space to test .strip()
    "Company Name": "Pytest Inc",
    "Role in Company": "QA",
    "Address": "123 Docker St",
    "Email": "bot@test.com",
    "Phone Number": "999888777"
  }

  result = process_round(driver_setup, dummy_data)

  assert result is True, "🟥 Falha ao processar a rodada (preencher/enviar)."
  print("-> Preenchimento de formulário:🟩 SUCESSO")