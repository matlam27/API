import mysql.connector

config = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'port': 3306,
  'database': 'API'
}

def get_database_connection():
  return mysql.connector.connect(**config)