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
    finally:
        if 'connection' in locals():
            connection.close()


test_database_connection()

with mysql.connector.connect(**config) as db :
    with db.cursor() as c:
        c.execute("insert into meteo (date, country, city, tmin, tmax, prcp, snow, swnd, awnd) \
                   values ('2023-09-20', 'FRANCE', 'Cergy', 41, 50, 0.54, 0.0, 0.0, 6.49)")
        db.commit()