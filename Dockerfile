# Use a imagem base oficial do Python 3.9
FROM python:3.9-slim

# Instale as dependências do sistema necessárias para compilar pacotes como mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de dependências para o contêiner
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do aplicativo para o contêiner
COPY . .

# Exponha a porta que o Flask vai utilizar
EXPOSE 5000

# Comando para rodar o aplicativo Flask com python3
CMD ["python3", "app/app.py"]
