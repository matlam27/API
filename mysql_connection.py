import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 8889,
    'database': 'API',
    'raise_on_warnings': True
}


def test_database_connection():
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connexion à la DB mySQL réussie")
    except mysql.connector.Error as err:
        print(f"erreur de connexion à la DB: {err}")
        if 'connection' in locals():
            connection.close()


test_database_connection()
