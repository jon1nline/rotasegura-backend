# Usar imagem Python slim (mais leve)
FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências do sistema necessárias para spaCy
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt


# Copiar código da aplicação
COPY . .

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput || true

# Expor porta (Hugging Face Spaces usa 7860 por padrão)
EXPOSE 7860

# Comando para iniciar a aplicação
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn --bind 0.0.0.0:7860 ccu.wsgi:application"]
