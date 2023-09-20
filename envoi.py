import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 8889,
    'database': 'API',
    'raise_on_warnings': True
}

with mysql.connector.connect(**config) as db:
    with db.cursor() as c:
        c.execute("insert into meteo (date, tmin, tmax, prcp, snow, swnd, awnd, country, city) \
                   values ('2023-09-20', 41, 50, 0.54, 0.0, 0.0, 6.49, 'FRANCE', 'Cergy')")
        db.commit()


