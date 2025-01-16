# Define a base image para o Python 3.9
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /code

# Copia o arquivo requirements.txt para o diretório de trabalho no container
COPY ./requirements.txt /code/requirements.txt

# Instala as dependências listadas no arquivo requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia todo o conteúdo da sua aplicação para o diretório de trabalho no container
COPY . /code

# Define o comando que será executado quando o container iniciar
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port", "5000", "--server.address", "0.0.0.0"]
