import mysql.connector

config = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'port': 3306,
  'database': 'API'
}

def get_database_connection():
  """
  Établit une connexion à la base de données MySQL en utilisant la configuration spécifiée.

  Returns:
      mysql.connector.connection.MySQLConnection: Objet de connexion à la base de données.
  """
  return mysql.connector.connect(**config)