import aiomysql

async def connect_to_database():
    # Configura le credenziali del database
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'NuovaPassword',
        'autocommit': True
    }

    # Crea una pool di connessioni al database
    pool = await aiomysql.create_pool(**db_config)

    return pool

async def create_database(pool, db_name):
    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            # Query per creare il database
            await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

async def create_tables(pool):
    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            # Query per creare le tabelle
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255),
                    email VARCHAR(255)
                )
            """)

# Esempio di utilizzo
async def main():
    # Connessione al database
    pool = await connect_to_database()

    # Creazione del database
    await create_database(pool, 'database_name')

    # Creazione delle tabelle
    await create_tables(pool)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
