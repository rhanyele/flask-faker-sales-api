# Projeto Flask Faker Sales API

Este projeto consiste em um sistema simples de processamento de transações usando Flask, onde transações fictícias são geradas utilizando a biblioteca Faker e enviadas para um servidor Flask. As transações são validadas com base em um modelo utilizando a biblioteca Pydantic e armazenadas em duas bases de dados Redis: uma para transações válidas e outra para transações inválidas. O sistema oferece endpoints para enviar transações via POST e recuperar transações válidas e inválidas via GET.

**Obs.:** O sistema gera tanto dados válidos quanto inválidos para que seja possível visualizar ambos os endpoints.

![flask-faker-sales-api](https://github.com/rhanyele/flask-faker-sales-api/assets/10997593/a85199ce-bb5e-447f-baea-4057108acf61)

## Estrutura do projeto
```bash
- logs
- src
  - app
    - database
      - redis_client.py
    - model
      - model.py
    - app.py
    - processing.py
  - client.py
- .python-version
- docker-compose.yml
- Dockerfile
- poetry.lock
- pyproject.toml
```

## Funcionalidades
- **Cliente:** Gera dados fictícios de transação usando a biblioteca Faker e envia transações fictícias para o servidor Flask via POST.
- **Validação de Transação:** Valida os dados recebidos utilizando modelo Pydantic.
- **Processamento:** Realiza o processamento das informações e separa as transações válidas e inválidas, além de calcular os campos necessários e inserir no banco de dados.
- **Cliente Redis:** Responsavel pela conexão, manipulação e consulta de dados no servidor Redis.
- **App:** O servidor Flask espera receber requisições POST contendo transações, envia para processamento e depois recupera os dados processados (tanto válidos quanto inválidos) através de requisições GET.

## Requisitos
- Python
- Poetry
- Flask
- Redis
- Docker

## Instalação
1. Clone este repositório:

   ```bash
   git clone https://github.com/rhanyele/flask-faker-sales-api.git
   ```

2. Acesse o diretório do projeto:

   ```bash
   cd flask-faker-sales-api
   ```

3. Instale as dependências usando Poetry:

   ```bash
   poetry install
   ```

4. Construa as imagens com docker compose:

   ```bash
   docker compose up
   ```

## Uso
1. Faça envio das transações através do ```client.py```:
   ```bash
   poetry run python .\src\client.py
   ```
- Com isso, você pode acessar os endpoints GET para visualizar os dados em formato JSON ou receber a requisição diretamente no arquivo ```client.py```.

## Endpoints
- **/apidocs:** Documentação da API com Swagger.
- **/upload_transaction:** Recebe transações em formato JSON, valida cada uma e as armazena como válidas ou inválidas.
- **/get_processed_valid_data:** Retorna as transações válidas armazenadas.
- **/get_processed_invalid_data:** Retorna as transações inválidas armazenadas.

## Contribuição
Sinta-se à vontade para contribuir com novos recursos, correções de bugs ou melhorias de desempenho. Basta abrir uma issue ou enviar um pull request!

## Autor
[Rhanyele Teixeira Nunes Marinho](https://github.com/rhanyele)

## Licença
Este projeto está licenciado sob a [MIT License](LICENSE).
