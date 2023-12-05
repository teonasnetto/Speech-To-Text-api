# Use a imagem oficial do Python como base
FROM python:3.11

# Crie e defina o diretório de trabalho no contêiner
WORKDIR /usr/src/app

# Copie os arquivos de dependências do projeto para o diretório de trabalho
COPY requirements.txt ./

# Instale as dependências, incluindo o FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos do projeto para o diretório de trabalho
COPY . .

# Exponha a porta em que a aplicação será executada
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
