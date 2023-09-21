import mysql.connector
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from mysql_connection import db

router = APIRouter()

compteur_ajouter_date = 0

class WeatherDate(BaseModel):
    date: str
    country: str
    city: str
    tmin: int = 0
    tmax: int = 0
    prcp: float = 0.0
    snow: float = 0.0
    snwd: float = 0.0
    awnd: float = 0.0

@router.post('/{date}/{country}/{city}/{tmin}/{tmax}/{prcp}/{snow}/{snwd}/{awnd}')
async def ajouter_date(
    date: str,
    country: str,
    city: str,
    tmin: int,
    tmax: int,
    prcp: float,
    snow: float,
    snwd: float,
    awnd: float
):
    """
        Cette fonction permet d'ajouter une nouvelle date avec des données météorologiques au fichier JSON.

        Args:
            date (str): La date à ajouter au format 'YYYY-MM-DD'.
            tmin (int): La température minimale.
            tmax (int): La température maximale.
            prcp (float): Les précipitations.
            snow (float): La quantité de neige.
            snwd (float): L'épaisseur de la neige.
            awnd (float): La vitesse du vent moyen.
            country (str): Le pays correspondant à la date.
            city (str): La ville correspondant à la date.

        Returns:
            dict: Un message indiquant le succès de l'opération et le nombre de requêtes pour ajouter une date.

        Raises:
            HTTPException: Si la date existe déjà dans le fichier JSON, une erreur HTTP 400 est renvoyée.

        Example:
            Pour ajouter la date '2022-05-28' avec des données météorologiques, vous pouvez accéder à cette URL avec une requête GET :
            http://127.0.0.1:8000/ajouter-date/2022-05-28/61/82/0.62/0.0/0.0/2.5
        """
    global compteur_ajouter_date
    compteur_ajouter_date += 1

    # Check if the date already exists in the database
    connection = db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM meteo WHERE date = %s", (date,))
    existing_data = cursor.fetchone()

    if existing_data:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail="La date existe déjà dans la base de données")

    new_date = WeatherDate(
        date=date,
        country=country,
        city=city,
        tmin=tmin,
        tmax=tmax,
        prcp=prcp,
        snow=snow,
        snwd=snwd,
        awnd=awnd
    )

    insert_weather_data(new_date)

    return {"message": "Date ajoutée avec succès", "compteur_ajouter_date": compteur_ajouter_date}

def insert_weather_data(weather_data):
    connection = db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO meteo (date, country, city, tmin, tmax, prcp, snow, snwd, awnd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (weather_data.date, weather_data.country, weather_data.city, weather_data.tmin, weather_data.tmax,
             weather_data.prcp, weather_data.snow, weather_data.snwd, weather_data.awnd))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting data into the database: {err}")
    finally:
        cursor.close()
        connection.close()