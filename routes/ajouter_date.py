import mysql.connector
from fastapi import APIRouter, HTTPException, Query

from database import config

router = APIRouter()

@router.post('/{annee}-{mois}-{jour}/{tmin}/{tmax}/{prcp}/{snow}/{swnd}/{awnd}/{country}/{city}')
async def ajouter_date(annee: str, mois: str, jour: str, tmin: int, tmax: int, prcp: float, snow: float, swnd: float, awnd: float, country: str, city: str):
    """
    Cette fonction permet de retourner à l'utilisateur la liste des météos correspondant à une ville qu'il rentre dans l'URL.
    :param city: (str) ville rentrée par l'utilisateur dans l'url
    :return:
    Une erreur en cas d'erreur ou la liste des données
    """
    try:
        date = f"{annee}-{mois}-{jour}"
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "INSERT INTO meteo (date, tmin, tmax, prcp, snow, swnd, awnd, country, city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                c.execute(query, (date, tmin, tmax, prcp, snow, swnd, awnd, country, city))
                result = c.fetchall()

                return {"ajouter_date": 'Sauvegarde effectué'}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
