import mysql.connector
from fastapi import APIRouter, HTTPException

from mysql_connection import config
from pydantic import BaseModel

router = APIRouter()

compteur_par_date = 0
compteur_par_date_specifique = {}

class WeatherData(BaseModel):
    date: str
    tmin: int
    tmax: int
    prcp: float
    snow: float
    snwd: float
    awnd: float
    id_city: int

@router.post('/{date}')
async def ajouter_date(date : str, weather_data: WeatherData):
    """
    Ajoute des données météorologiques pour une date spécifique à la base de données.

    Args:
        date (str): La date au format 'AAAA-MM-JJ'.
        weather_data (WeatherData): Les données météorologiques à ajouter, conformes au modèle WeatherData.

    Returns:
        dict: Un dictionnaire contenant les informations suivantes :
            - {"ajouter_date": "Sauvegarde effectuée"} en cas de succès.
            - {"nombre_requetes_par_date": compteur_par_date, "nombre_requetes_par_date_specifique": compteur_par_date_specifique} pour le suivi du nombre de requêtes par date.

    Raises:
        HTTPException (500): Si une erreur de base de données se produit.
    """
    tmin = weather_data.tmin
    tmax = weather_data.tmax
    prcp = weather_data.prcp
    snow = weather_data.snow
    snwd = weather_data.snwd
    awnd = weather_data.awnd
    id_city = weather_data.id_city

    try:
        global compteur_par_date
        compteur_par_date += 1

        compteur_par_date_specifique[date] = compteur_par_date_specifique.get(date, 0) + 1

        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "INSERT INTO meteo (date, tmin, tmax, prcp, snow, snwd, awnd, id_city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                c.execute(query, (date, tmin, tmax, prcp, snow, snwd, awnd, id_city))
                result = c.fetchall()

                return {"ajouter_date": 'Sauvegarde effectué',
                        "nombre_requetes_par_date": compteur_par_date, "nombre_requetes_par_date_specifique": compteur_par_date_specifique}

    except mysql.connector.Error as err:
        # Gérer les erreurs de base de données
        raise HTTPException(status_code=500, detail=f"Database error: {err}")