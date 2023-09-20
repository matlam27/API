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
  return mysql.connector.connect(**config)