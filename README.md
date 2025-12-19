# Market Data API (Proxy Service)

## 1. Sobre o Projeto
Este microsserviço atua como um **Proxy Service** na arquitetura do sistema InvestMonitor. Sua responsabilidade é isolar a comunicação com provedores de dados externos, entregando dados normalizados e limpos para o sistema principal.

O projeto foi desenvolvido seguindo o padrão REST, garantindo baixo acoplamento e alta coesão.

### API Externa Utilizada
* **Serviço:** Yahoo Finance.
* **Biblioteca:** `yfinance` (Wrapper não oficial).
* **Custo/Licença:** Gratuito para uso educacional/pessoal. Não requer chave de API (API Key) para consultas básicas.
* **Tratamento de Dados:** A API intercepta os dados brutos do Yahoo, normaliza os tickers para o padrão da B3 (adicionando `.SA`) e trata erros de conexão antes de responder ao cliente.

## 2. Tecnologias
* **Linguagem:** Python 3.12
* **Framework:** FastAPI
* **Servidor:** Uvicorn
* **Containerização:** Docker

## 3. Endpoints Disponíveis
A API fornece 4 rotas públicas (Método GET):

| Rota | Descrição | Parâmetros |
| :--- | :--- | :--- |
| `/health` | Monitoramento de saúde do serviço (Healthcheck). | N/A |
| `/price/{ticker}` | Retorna o preço de fechamento mais recente. | `ticker`: Código do ativo (ex: PETR4). |
| `/info/{ticker}` | Retorna metadados (Setor, Moeda, Nome Longo). | `ticker`: Código do ativo. |
| `/history/{ticker}` | Retorna histórico de preços dos últimos 5 dias. | `ticker`: Código do ativo. |

## 4. Instruções de Instalação e Execução

### Opção A: Via Docker (Recomendado)
Garante que o ambiente seja idêntico ao de desenvolvimento.

1.  Construa a imagem:
    ```bash
    docker build -t market-data-api .
    ```
2.  Inicie o container na porta 5000:
    ```bash
    docker run -p 5000:5000 market-data-api
    ```
3.  Acesse a documentação interativa (Swagger):
    * http://localhost:5000/docs

### Opção B: Execução Local (Sem Docker)
Para execução em ambiente de desenvolvimento Python padrão.

1.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv .venv
    # Linux/Mac:
    source .venv/bin/activate
    # Windows:
    # .venv\Scripts\activate
    ```
2.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3.  Execute o servidor:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 5000
    ```

---
*Projeto desenvolvido para a disciplina de Arquitetura de Software - MVP.*