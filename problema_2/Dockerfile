FROM postgres:16

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

COPY extract_pokemon_to_postgres.py /app/extract_pokemon_to_postgres.py
COPY verificar_amostras.sql /app/verificar_amostras.sql
COPY docker-entrypoint-load.sh /usr/local/bin/docker-entrypoint-load.sh
RUN chmod +x /usr/local/bin/docker-entrypoint-load.sh

ENV PGHOST=127.0.0.1
ENV PGPORT=5432

EXPOSE 5432

ENTRYPOINT ["/usr/local/bin/docker-entrypoint-load.sh"]
