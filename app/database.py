import aiomysql
import pymysql

class DatabaseManager:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    async def connect(self):
        # Configura le credenziali del database
        db_config = {
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password,
            'autocommit': True
        }

        # Crea una pool di connessioni al database
        self.pool = await aiomysql.create_pool(**db_config)

    async def execute_query(self, query, db_name=None):
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                # Seleziona il database se specificato
                if db_name:
                    await cursor.execute(f"USE {db_name}")
                # Esegui la query
                await cursor.execute(query)
                result = await cursor.fetchall()
                return result

    async def create_database(self, db_name):
        try:
            # Crea il database se non esiste già
            await self.execute_query(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        except pymysql.err.OperationalError as e:
            if e.args[0] == 1007:  # MySQL error code for "database exists"
                print(f"Database '{db_name}' already exists")
            else:
                raise  # Rilancia l'eccezione se non è un errore di database esistente

    async def create_tables(self, db_name):
        try:
            # Seleziona il database
            await self.execute_query(f"USE {db_name}")

            # Definizione delle tabelle da creare
            tables_to_create = {
                'users': """
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255),
                        email VARCHAR(255)
                    )
                """,
                'posts': """
                    CREATE TABLE IF NOT EXISTS posts (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255),
                        content TEXT,
                        user_id INT,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """
                # Aggiungi altre definizioni di tabella qui se necessario
            }

            # Ottieni elenco delle tabelle esistenti nel database
            existing_tables = await self.execute_query("SHOW TABLES")
            existing_tables = [table[0] for table in existing_tables]

            # Loop attraverso le definizioni delle tabelle e crea solo quelle mancanti
            for table_name, table_definition in tables_to_create.items():
                if table_name not in existing_tables:
                    # Crea la tabella solo se non esiste già
                    await self.execute_query(table_definition)
        except pymysql.err.OperationalError as e:
            print(f"Errore durante la creazione delle tabelle: {e}")

# Esempio di utilizzo
async def main():
    db_manager = DatabaseManager('localhost', 3306, 'root', 'NuovaPassword')
    await db_manager.connect()

    # Creazione del database
    await db_manager.create_database('test_001_db')

    # Creazione delle tabelle nel database specificato
    await db_manager.create_tables('test_001_db')

    # Esegui una query al database
    result = await db_manager.execute_query("SELECT * FROM users", 'test_001_db')
    print(result)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
