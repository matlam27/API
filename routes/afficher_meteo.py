import mysql
from fastapi import APIRouter, HTTPException

from mysql_connection import config

router = APIRouter()

compteur_afficher_donnees = 0

@router.get('/')
async def afficher_meteo_date():
    try:
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "SELECT * FROM meteo"
                c.execute(query)
                result = c.fetchall()

                if not result:
                    raise HTTPException(status_code=404, detail="Data not found")

                # Convert the result to a list of dictionaries
                data = [dict(zip(c.column_names, row)) for row in result]

                return {"meteo_data": data}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")