import mysql.connector
from fastapi import APIRouter, HTTPException, Query

from mysql_connection import config

router = APIRouter()


@router.get('/{country}/{id_country}')
async def country_date(id_country: int):
    """
        Cette fonction permet de retourner à l'utilisateur la liste des météos correspondant à un pays qu'il rentre dans l'URL.
        :param country: (str) pays rentré par l'utilisateur dans l'url
        :return:
        Une erreur en cas d'erreur ou la liste des données correspondant au pays entré par l'utilisateur.
        """
    try:
        # Connect to the database
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                # Build and execute the SQL query with a parameter
                query = "SELECT meteo.*, country.name AS country_name FROM meteo JOIN country ON meteo.id_country = country.id WHERE meteo.id_country = %s"
                c.execute(query, (id_country,))
                result = c.fetchall()

                # Check if any results were found
                if not result:
                    raise HTTPException(status_code=404, detail="Data not found")

                # Convert the result to a list of dictionaries
                data = [dict(zip(c.column_names, row)) for row in result]

                return {"country_data": data}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
