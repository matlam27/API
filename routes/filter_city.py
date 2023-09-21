import mysql.connector
from fastapi import APIRouter, HTTPException, Query

from database import config

router = APIRouter()


@router.get('/{city}')
async def city_date(city: str):
    """
    Cette fonction permet de retourner à l'utilisateur la liste des météos correspondant à une ville qu'il rentre dans l'URL.
    :param city: (str) ville rentrée par l'utilisateur dans l'url
    :return:
    Une erreur en cas d'erreur ou la liste des données
    """
    try:
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "SELECT * FROM meteo WHERE city = %s"
                c.execute(query, (city,))
                result = c.fetchall()

                if not result:
                    raise HTTPException(status_code=404, detail="Data not found")

                # Convert the result to a list of dictionaries
                data = [dict(zip(c.column_names, row)) for row in result]

                return {"city_data": data}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
