import mysql.connector
from fastapi import APIRouter, HTTPException, Query

from mysql_connection import config

router = APIRouter()


@router.get('/{id_city}')
async def city_date(id_city: int):
    """
    Cette fonction permet de retourner à l'utilisateur la liste des météos correspondant à une ville qu'il rentre dans l'URL.
    :param city: (str) ville rentrée par l'utilisateur dans l'url
    :return:
    Un tableau de données correspondant aux données de l'utilisateur
    Une erreur en cas d'erreur
    """
    try:
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "SELECT meteo.*, city.name AS city_name FROM meteo JOIN city ON meteo.id_city = city.id WHERE meteo.id_city = %s"
                c.execute(query, (id_city, ))
                result = c.fetchall()

                if not result:
                    raise HTTPException(status_code=404, detail="Data not found")

                # Convert the result to a list of dictionaries
                data = [dict(zip(c.column_names, row)) for row in result]

                return {"city_data": data}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
