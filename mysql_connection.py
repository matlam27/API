import mysql.connector

config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'port': 8889,
  'database': 'test',
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)

cursor = cnx.cursor(dictionary=True)

cursor.execute('SELECT `id`, `name` FROM `test`')

results = cursor.fetchall()

for row in results:
  id = row['id']
  title = row['name']
  print '%s | %s' % (id, title)

cnx.close()