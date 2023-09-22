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
        c.execute("insert into meteo (date, tmin, tmax, prcp, snow, snwd, awnd, id_city) \
                   values ('2023-09-20', 41, 50, 1, 0.0, 0.0, 6.49, 1)")
        db.commit()