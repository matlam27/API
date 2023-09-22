import mysql.connector

config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'API2',
    'raise_on_warnings': True
}

def test_database_connection():
    """
    Teste la connexion à la base de données MySQL en utilisant la configuration spécifiée.

    Raises:
        Exception: Levée en cas d'erreur de connexion à la base de données.
    """
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connexion à la base de données MySQL réussie")
    except mysql.connector.Error as err:
        raise Exception(f"Erreur de connexion à la base de données : {err}")
    finally:
        if 'connection' in locals():
            connection.close()

test_database_connection()