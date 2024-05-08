from fastapi import FastAPI
from database import connect_to_database, execute_query

app = FastAPI()

# Endpoint per la lettura di tutti gli utenti
@app.get("/users")
async def read_users():
    # Connessione al database
    pool = await connect_to_database()

    # Esegui una query al database
    query = "SELECT * FROM users"
    result = await execute_query(pool, query)

    return result
