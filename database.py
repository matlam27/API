import mysql.connector

config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'port': 8000,
  'database': 'test',
  'raise_on_warnings': True
}

def get_database_connection():
  """
  Établit et retourne une connexion à la base de données MySQL.

  Returns:
      mysql.connector.connection.MySQLConnection: Objet de connexion à la base de données.
  """
  return mysql.connector.connect(**config)
