-- 5 linhas de cada tabela (apos a carga no Postgres)
SELECT * FROM generation ORDER BY id LIMIT 5;
SELECT * FROM pokemon ORDER BY id LIMIT 5;
SELECT * FROM ability ORDER BY id LIMIT 5;
SELECT * FROM move ORDER BY id LIMIT 5;
SELECT * FROM pokemon_ability ORDER BY pokemon_id, ability_id LIMIT 5;
SELECT * FROM pokemon_move ORDER BY pokemon_id, move_id LIMIT 5;
