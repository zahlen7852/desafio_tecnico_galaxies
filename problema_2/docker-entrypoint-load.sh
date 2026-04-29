#!/bin/bash
set -e

# Inicia o Postgres em segundo plano usando o entrypoint oficial da imagem.
docker-entrypoint.sh postgres &
POSTGRES_PID=$!

echo "Aguardando o Postgres aceitar conexoes..."
until pg_isready -h 127.0.0.1 -p 5432 -U "${POSTGRES_USER:-postgres}" >/dev/null 2>&1; do
  sleep 1
done

echo "Postgres no ar. Executando o script de ETL dos Pokemons..."
export PGHOST=127.0.0.1
export PGPORT=5432
export PGUSER="${POSTGRES_USER:-postgres}"
export PGPASSWORD="${POSTGRES_PASSWORD:-postgres}"
export PGDATABASE="${POSTGRES_DB:-pokemon_db}"

/opt/venv/bin/python /app/extract_pokemon_to_postgres.py

echo ""
echo "---- Verificacao: 5 linhas de cada tabela ----"

echo ""
echo "Executando: SELECT * FROM generation ORDER BY id LIMIT 5;"
psql -h 127.0.0.1 -p 5432 -U "${PGUSER}" -d "${PGDATABASE}" -c "SELECT * FROM generation ORDER BY id LIMIT 5;"

echo ""
echo "Executando: SELECT * FROM pokemon ORDER BY id LIMIT 5;"
psql -h 127.0.0.1 -p 5432 -U "${PGUSER}" -d "${PGDATABASE}" -c "SELECT * FROM pokemon ORDER BY id LIMIT 5;"

echo ""
echo "Executando: SELECT * FROM ability ORDER BY id LIMIT 5;"
psql -h 127.0.0.1 -p 5432 -U "${PGUSER}" -d "${PGDATABASE}" -c "SELECT * FROM ability ORDER BY id LIMIT 5;"

echo ""
echo "Executando: SELECT * FROM move ORDER BY id LIMIT 5;"
psql -h 127.0.0.1 -p 5432 -U "${PGUSER}" -d "${PGDATABASE}" -c "SELECT * FROM move ORDER BY id LIMIT 5;"

echo ""
echo "Executando: SELECT * FROM pokemon_ability ORDER BY pokemon_id, ability_id LIMIT 5;"
psql -h 127.0.0.1 -p 5432 -U "${PGUSER}" -d "${PGDATABASE}" -c "SELECT * FROM pokemon_ability ORDER BY pokemon_id, ability_id LIMIT 5;"

echo ""
echo "Executando: SELECT * FROM pokemon_move ORDER BY pokemon_id, move_id LIMIT 5;"
psql -h 127.0.0.1 -p 5432 -U "${PGUSER}" -d "${PGDATABASE}" -c "SELECT * FROM pokemon_move ORDER BY pokemon_id, move_id LIMIT 5;"

echo ""
echo "ETL finalizado. Mantendo o Postgres em execucao..."
wait "${POSTGRES_PID}"
