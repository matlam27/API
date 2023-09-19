from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json

router = APIRouter()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

compteur_ajouter_date = 0


class WeatherDate(BaseModel):
    date: str
    tmin: int = 0
    tmax: int = 0
    prcp: float = 0.0
    snow: float = 0.0
    snwd: float = 0.0
    awnd: float = 0.0


@router.post('/{date}/{tmin}/{tmax}/{prcp}/{snow}/{snwd}/{awnd}')
async def ajouter_date(
    date: str,
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

    for data in weather_data:
        if data['date'] == date:
            raise HTTPException(
                status_code=400, detail="La date existe déjà dans le fichier JSON")

    new_date = WeatherDate(
        date=date,
        tmin=tmin,
        tmax=tmax,
        prcp=prcp,
        snow=snow,
        snwd=snwd,
        awnd=awnd
    )

    weather_data.append(new_date.dict())

    with open('rdu-weather-history.json', 'w') as json_file:
        json.dump(weather_data, json_file, indent=4)

    return {"message": "Date ajoutée avec succès", "compteur_ajouter_date": compteur_ajouter_date}
