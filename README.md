# 🤖 FormSeeker

![CI Status](https://github.com/GustavoMartin2002/FormSeeker/actions/workflows/ci.yml/badge.svg)
![Docker](https://img.shields.io/badge/DevOps%20-Docker-blue)
![Python](https://img.shields.io/badge/Python%20-3.7-yellow)
![Selenium](https://img.shields.io/badge/Framework%20-Selenium-red)
![Pytest](https://img.shields.io/badge/Framework%20-Pytest-red)
![Pandas](https://img.shields.io/badge/Lib%20-Pandas-purple)
![Openpyxl](https://img.shields.io/badge/Lib%20-Openpyxl-purple)

Esta solução é um **BOT** de automação (RPA) desenvolvido para resolver o [RPA Challenge](https://rpachallenge.com/). O objetivo é demonstrar proficiência na criação de automações robustos, estáveis e imunes a mudanças estruturais.

O FormSeeker utiliza uma estratégia avançada de localização de elementos para garantir que o preenchimento seja 100% preciso em todas as 10 rodadas, independentemente da posição aleatória dos campos na tela.

### 💻 Tecnologias Utilizadas
- **Python 3.7+:** Linguagem Principal e Lógica de Negócio.
- **Selenium:** Motor de Automação Web.
- **Pandas / OpenPyXL:** Manipulação de Dados Estruturados.
- **Pytest:** Framework de Testes.
- **Docker & Docker Compose:** Isolamento e Orquestração do Ambiente.

---

### 💡Descrição Detalhada e Funcionalidades
#### Arquitetura:
O projeto segue a arquitetura de Micro-serviços Light via Docker Compose para isolamento e reprodutibilidade:
- Serviço `selenium-chrome`: Container dedicado que executa o navegador Google Chrome (e o servidor VNC) para a automação.
- Serviço `app`: Container leve que executa o código Python, agindo como o cliente do Selenium.

#### Fluxo:
- **Orquestração:** `docker-compose` inicia o Chrome e só depois do `healthcheck` inicia o container `app`.
- **UX Delay:** O robô exibe uma contagem regressiva de 10s no terminal, dando tempo ao usuário para abrir o VNC `localhost:7900`.
- **Leitura:** O `main.py` aciona a leitura da planilha (pandas).
- **Automação:** O BOT navega, clica em Start, e então entra no loop das 10 rodadas.

#### Estratégia:
A **abordagem** para lidar com os **elementos dinâmicos** foi a utilização de **Seletores Relativos baseados na vizinhança (Sibling XPath).**
- **Problema:** Os IDs `id="c81xn"` mudam e o atributo `for` (que liga o `<label>` ao `<input>`) está ausente ou é imprevisível.
- **Solução:** O bot ignora os IDs e procura o campo de entrada `<input>` que é vizinho (irmão) da etiqueta `<label>` que contém o texto exato da planilha.
```
//label[normalize-space(text())='{NomeCampo}']/following-sibling::input
```

---

### 🧪 Testes
O projeto utiliza **pytest** para validar todas as quatro funções do `automation_core.py` (`read_spreadsheet`, `start_driver`, `start_challenge` e `process_round`). Os testes são de Integração, pois comprovam o funcionamento do navegador real.

---

### 🔄 CI/CD
A saúde do código é verificada automaticamente pelo GitHub Actions.
- **Localização:** O arquivo de workflow se encontra em `.github/workflows/ci.yml`.
- **Comando de CI:** O pipeline executa o comando de teste mais robusto: `docker-compose -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from app`.
- **Finalidade:** Garante que a branch `main` só receba código que passou 100% nos testes de integração.

---

### 🛠️ Requisitos e Configuração de Ambiente
O projeto é containerizado, minimizando as dependências do sistema operacional:

#### 1. 📋 Pré-requisitos
- **Docker Desktop:** Instale e garanta que ele esteja rodando no seu sistema (Windows/macOS/Linux).
- **Git:** Para clonar o repositório.

#### 2. 📥 Instalação e Preparação
Abra o seu terminal (ou Git Bash) e clone o repositório:
```
git clone https://github.com/GustavoMartin2002/FormSeeker.git
cd FormSeeker
```
*(Se preferir, pode simplesmente fazer o download do arquivo ZIP e descompactá-lo.)*

#### 3. ⚙️ Como Iniciar a Aplicação
- **1. Inicialização:**  <br>
O Docker sobe o Chrome (Selenium) e o `app` (BOT), esperando a prontidão do servidor (healthcheck).
```
  docker-compose up --abort-on-container-exit
```

- **2. Contagem:** <br>
O **BOT** inicia uma contagem regressiva de **10 segundos** no terminal.

- **3. Ação do Usuário:** <br>
Acesse: http://localhost:7900 para ver a tela do BOT.

- **4. Execução:** <br>
Após os 10 segundos, a automação começa a preencher as 10 rodadas.

- **5. Encerramento** <br>
O container vai ser parado pela flag `--abort-on-container-exit` inserida no primeiro passo.

#### 4. 🧪 Como Rodar os Testes Automatizados
Usa o arquivo de teste dedicado `docker-compose.test.yml` para validar se a lógica de localização de elementos (a estratégia Sibling XPath) e a conexão estão funcionando.
```
  docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```
- O Docker sobe o Selenium e o `app` (mas, desta vez, o `app` roda o `pytest`).
- O Pytest executa as verificações (leitura de arquivo, conexão e interação).
- Quando os testes acabam, o Docker fecha o navegador automaticamente.
- O terminal mostra `5 passed` e a mensagem de encerramento.

---

### 📝 Considerações Finais
O projeto foi construído com foco em **modularização** **(pastas** `functions` **e** `tests`**)** e **legibilidade**. A escolha do **Docker** e do **healthcheck** visa o máximo de **reprodutibilidade** e **estabilidade**.
