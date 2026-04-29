import os
import requests
import psycopg2

BASE_URL = "https://pokeapi.co/api/v2"


def get_all_pokemon_urls(limit=100):
    urls = []
    offset = 0

    while True:
        page_url = f"{BASE_URL}/pokemon?limit={limit}&offset={offset}"
        response = requests.get(page_url, timeout=30)
        response.raise_for_status()
        data = response.json()

        for item in data.get("results", []):
            urls.append(item["url"])

        if data.get("next") is None:
            break

        offset += limit

    return urls


def parse_pokemon(pokemon_data, species_data):
    return {
        "id": pokemon_data["id"],
        "name": pokemon_data["name"],
        "base_experience": pokemon_data.get("base_experience"),
        "height": pokemon_data.get("height"),
        "weight": pokemon_data.get("weight"),
        "generation": species_data["generation"]["name"],
        "abilities": [a["ability"]["name"] for a in pokemon_data.get("abilities", [])],
        "moves": [m["move"]["name"] for m in pokemon_data.get("moves", [])],
    }


def get_all_pokemon_parsed(limit=100):
    parsed_pokemon = []
    pokemon_urls = get_all_pokemon_urls(limit=limit)

    for index, pokemon_url in enumerate(pokemon_urls, start=1):
        pokemon_response = requests.get(pokemon_url, timeout=30)
        pokemon_response.raise_for_status()
        pokemon_data = pokemon_response.json()

        species_url = pokemon_data["species"]["url"]
        species_response = requests.get(species_url, timeout=30)
        species_response.raise_for_status()
        species_data = species_response.json()

        parsed_pokemon.append(parse_pokemon(pokemon_data, species_data))

        if index % 50 == 0:
            print(f"Processados (API): {index}")

    return parsed_pokemon


def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS generation (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS pokemon (
                id INT PRIMARY KEY,
                name TEXT NOT NULL,
                base_experience INT,
                height INT,
                weight INT,
                generation_id INT NOT NULL REFERENCES generation(id)
            );

            CREATE TABLE IF NOT EXISTS ability (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS move (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS pokemon_ability (
                pokemon_id INT NOT NULL REFERENCES pokemon(id),
                ability_id INT NOT NULL REFERENCES ability(id),
                PRIMARY KEY (pokemon_id, ability_id)
            );

            CREATE TABLE IF NOT EXISTS pokemon_move (
                pokemon_id INT NOT NULL REFERENCES pokemon(id),
                move_id INT NOT NULL REFERENCES move(id),
                PRIMARY KEY (pokemon_id, move_id)
            );
            """
        )
    conn.commit()


def get_or_create_generation_id(cur, generation_name):
    cur.execute(
        """
        INSERT INTO generation (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id
        """,
        (generation_name,),
    )
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute("SELECT id FROM generation WHERE name = %s", (generation_name,))
    return cur.fetchone()[0]


def get_or_create_ability_id(cur, ability_name):
    cur.execute(
        """
        INSERT INTO ability (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id
        """,
        (ability_name,),
    )
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute("SELECT id FROM ability WHERE name = %s", (ability_name,))
    return cur.fetchone()[0]


def get_or_create_move_id(cur, move_name):
    cur.execute(
        """
        INSERT INTO move (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id
        """,
        (move_name,),
    )
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute("SELECT id FROM move WHERE name = %s", (move_name,))
    return cur.fetchone()[0]


def save_pokemon_data(conn, parsed_pokemon):
    with conn.cursor() as cur:
        for index, p in enumerate(parsed_pokemon, start=1):
            generation_id = get_or_create_generation_id(cur, p["generation"])

            cur.execute(
                """
                INSERT INTO pokemon (id, name, base_experience, height, weight, generation_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    base_experience = EXCLUDED.base_experience,
                    height = EXCLUDED.height,
                    weight = EXCLUDED.weight,
                    generation_id = EXCLUDED.generation_id
                """,
                (
                    p["id"],
                    p["name"],
                    p["base_experience"],
                    p["height"],
                    p["weight"],
                    generation_id,
                ),
            )

            cur.execute("DELETE FROM pokemon_ability WHERE pokemon_id = %s", (p["id"],))
            for ability_name in p["abilities"]:
                ability_id = get_or_create_ability_id(cur, ability_name)
                cur.execute(
                    """
                    INSERT INTO pokemon_ability (pokemon_id, ability_id)
                    VALUES (%s, %s)
                    ON CONFLICT (pokemon_id, ability_id) DO NOTHING
                    """,
                    (p["id"], ability_id),
                )

            cur.execute("DELETE FROM pokemon_move WHERE pokemon_id = %s", (p["id"],))
            for move_name in p["moves"]:
                move_id = get_or_create_move_id(cur, move_name)
                cur.execute(
                    """
                    INSERT INTO pokemon_move (pokemon_id, move_id)
                    VALUES (%s, %s)
                    ON CONFLICT (pokemon_id, move_id) DO NOTHING
                    """,
                    (p["id"], move_id),
                )

            if index % 50 == 0:
                conn.commit()
                print(f"Salvos no Postgres: {index}")

    conn.commit()


def main():
    db_host = os.getenv("PGHOST", "localhost")
    db_port = int(os.getenv("PGPORT", "5432"))
    db_name = os.getenv("PGDATABASE", "pokemon_db")
    db_user = os.getenv("PGUSER", "postgres")
    db_password = os.getenv("PGPASSWORD", "postgres")

    print("Extraindo dados da PokeAPI...")
    parsed_pokemon = get_all_pokemon_parsed(limit=100)
    print(f"Total extraído: {len(parsed_pokemon)}")

    print("Conectando ao Postgres...")
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password,
    )

    try:
        print("Criando tabelas...")
        create_tables(conn)

        print("Salvando dados...")
        save_pokemon_data(conn, parsed_pokemon)
        print("Finalizado com sucesso.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
