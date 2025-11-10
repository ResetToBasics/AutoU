# Dockerfile para containerizar a aplicação
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de requisitos
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório de uploads
RUN mkdir -p uploads

# Expor porta
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_ENV=production
ENV FLASK_DEBUG=false
ENV PYTHONUNBUFFERED=1

# Comando para iniciar a aplicação
CMD ["python", "run.py"]

