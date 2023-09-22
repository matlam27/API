from fastapi import FastAPI
from routes import router as routes_router
from database import get_database_connection

app = FastAPI()

app.include_router(routes_router)

def get_db_conn():
    """
    Établit une connexion à la base de données et la fournit en tant que générateur.

    Yields:
        mysql.connector.connection.MySQLConnection: Objet de connexion à la base de données.
    """
    conn = get_database_connection()
    try:
        yield conn
    finally:
        conn.close()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
