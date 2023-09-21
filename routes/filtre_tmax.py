from fastapi import APIRouter, HTTPException
from mysql_connection import config
import mysql.connector
from mysql_connection import config
import mysql.connector
import json

router = APIRouter()

compteur_filtrer_date = 0
compteur_filtrer_temp = 0

compteur_dates = {}
compteur_temp = {}

@router.get('/{args}')
async def filtre_tmax(args: int):
    """
    Cette fonction permet de filtrer les dates en fonction de la température minimale.

    Args:
        args (int): La température maximale à utiliser comme critère de filtrage.

    Returns:
        dict: Une liste des dates qui ont une température maximale égale à l'argument spécifié,
              ainsi que le nombre total de requêtes pour filtrer des températures et le nombre de requêtes pour cette température spécifique.

    Example:
        Pour filtrer les dates avec une température maximale de 82, vous pouvez accéder à cette URL avec une requête GET :
        http://127.0.0.1:8000/temp/82
        http://127.0.0.1:8000/temp/82
    """
    global compteur_filtrer_temp
    compteur_filtrer_temp += 1

    # Incrémente le compteur pour cette température spécifique
    compteur_temp[args] = compteur_temp.get(args, 0) + 1

    try:
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                # Utilisez une requête SQL avec une clause WHERE pour filtrer par tmin
                query = "SELECT * FROM meteo WHERE tmax = %s"
                c.execute(query, (args,))
                result = c.fetchall()

                if not result:
                    raise HTTPException(status_code=404, detail="Data not found")

                # Convert the result to a list of dictionaries
                data = [dict(zip(c.column_names, row)) for row in result]

                return {"meteo_data": data}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
