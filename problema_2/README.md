# Problema 2

Usei um modelo normalizado para evitar dados repetidos e manter organização.
A tabela pokemon guarda os dados principais de cada Pokémon.
As tabelas ability e move guardam os catálogos de habilidades passivas e golpes.
A tabela generation guarda a geração de cada Pokémon, e pokemon se conecta a ela pelo generation_id.
Como um Pokémon pode ter várias habilidades e vários golpes, usei tabelas de associação (pokemon_ability e pokemon_move) para representar essas relações.

Fato: 

    pokemon:
     Colunas:
            id
            name
            base_experience
            height
            weight
            generation_id

Dimensões:

    generation:
     Colunas: 
            id
            name
    
    ability:
     Colunas:
            id
            name
    
    move:  
     Colunas:
             id
             name
    
Associativas:

    pokemon_ability:
     Colunas:
             pokemon_id
             ability_id

    pokemon_move:
     Colunas:
             pokemon_id
             move_id


# Como rodar 

#primeiro comando
docker build -t pokemon-etl-postgres ./problema_2

#segundo comando (aqui os dados não estão persistidos, não estou criando nenhum volume)
docker run --name pokemon-etl \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=pokemon_db \
  -p 5432:5432 \
  pokemon-etl-postgres

#terceiro comando - se conectar no container
docker exec -it pokemon-etl sh

#quarto comando - abrir o postgres
psql -U postgres -d pokemon_db

#quinto comando - verificar as tabelas  - 
eu coloquei para rodar uma query no final da execução mostrando 5 linhas de cada tabela, mas se for necessário, podem rodar alguma query no postgres

Exemplo opcional com nomes (Pokemon + geracao):

```sql
SELECT p.id, p.name, g.name AS generation
FROM pokemon p
JOIN generation g ON g.id = p.generation_id
ORDER BY p.id
LIMIT 5;
```
