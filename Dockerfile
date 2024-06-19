# Use a imagem oficial do Python como base
FROM python:3.12.2

# Instale o Poetry
RUN pip install poetry

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo pyproject.toml e poetry.lock para o diretório de trabalho
COPY pyproject.toml poetry.lock ./

# Instale as dependências do projeto
RUN poetry install --no-root

# Copie apenas o conteúdo da pasta app para o diretório de trabalho
COPY src/app app

# Crie o diretório de logs
RUN mkdir -p /app/logs

# Defina a variável de ambiente para informar ao Flask o aplicativo a ser executado
ENV FLASK_APP=app/app.py

# Exponha a porta que o Flask usará
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
