from fastapi import APIRouter, HTTPException
from mysql_connection import config
import mysql.connector
import json

router = APIRouter()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

compteur_filtrer_date = 0
compteur_filtrer_temp = 0

compteur_dates = {}
compteur_temp = {}

@router.get('/date/{annee}-{mois}-{jour}')
async def filtrer_date(annee: int, mois: int, jour: int):
    """
    Cette fonction permet d'afficher les données pour une date spécifique.

    Args:
        annee (int): L'année de la date à afficher.
        mois (int): Le mois de la date à afficher.
        jour (int): Le jour de la date à afficher.

    Returns:
        dict: Les données de la date demandée, le nombre total de requêtes pour filtrer des dates et le nombre de requêtes pour cette date spécifique.

    Raises:
        HTTPException: Si la date n'est pas trouvée dans le fichier JSON, une erreur HTTP 404 est générée.
    """
    
    try:
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                # Utilisez une requête SQL avec une clause WHERE pour filtrer par date
                query = "SELECT * FROM meteo WHERE YEAR(date) = %s AND MONTH(date) = %s AND DAY(date) = %s"
                c.execute(query, (annee, mois, jour))
                result = c.fetchall()

                if not result:
                    raise HTTPException(status_code=404, detail="Data not found")

                # Convert the result to a list of dictionaries
                data = [dict(zip(c.column_names, row)) for row in result]

                return {"meteo_data": data}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

@router.get('/temp/{args}')
async def filtrer_temp(args: int):
    """
    Cette fonction permet de filtrer les dates en fonction de la température maximale.

    Args:
        args (int): La température maximale à utiliser comme critère de filtrage.

    Returns:
        dict: Une liste des dates qui ont une température maximale égale à l'argument spécifié,
              ainsi que le nombre total de requêtes pour filtrer des températures et le nombre de requêtes pour cette température spécifique.

    Example:
        Pour filtrer les dates avec une température maximale de 82, vous pouvez accéder à cette URL avec une requête GET :
        http://127.0.0.1:8000/temp/82
    """
    global compteur_filtrer_temp
    compteur_filtrer_temp += 1

    # Incrémente le compteur pour cette température spécifique
    compteur_temp[args] = compteur_temp.get(args, 0) + 1

    dates = []
    for data in weather_data:
        if data['tmax'] == args:
            dates.append(data)
    return {"nombre_requetes_filtrer_temp": compteur_filtrer_temp,
            "nombre_requetes_date_specifique": compteur_temp[args], "weather_data": dates}