from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

class WeatherDate(BaseModel):
    date: str
    tmin: int = 0
    tmax: int = 0
    prcp: float = 0.0
    snow: float = 0.0
    snwd: float = 0.0
    awnd: float = 0.0

@app.get('/donnees')
async def afficher_donnees():
    """Cette fonction permet d'afficher toutes les dates présentes dans le fichier json."""
    return weather_data

@app.get('/ajouter-date/{date_to_add}')
async def ajouter_date(date_to_add: str):
    """
    Cette fonction permet d'ajouter une nouvelle date au fichier JSON ou de mettre à jour une date existante.

    Args:
        date_to_add (str): La date à ajouter ou à mettre à jour au format 'YYYY-MM-DD'.

    Returns:
        dict: Un message indiquant le succès de l'opération.

    Raises:
        HTTPException: Si la date existe déjà dans le fichier JSON, une erreur HTTP 400 est renvoyée.

    Example:
        Pour ajouter la date '2023-09-19', vous pouvez accéder à cette URL avec une requête GET :
        http://127.0.0.1:8000/ajouter-date/2023-09-19
    """
    if date_to_add in weather_data:
        raise HTTPException(status_code=400, detail="La date existe déjà dans le fichier JSON")

    weather_data.append(date_to_add)

    with open('rdu-weather-history.json', 'w') as json_file:
        json.dump(weather_data, json_file, indent=4)

    return {"message": "Date ajoutée avec succès"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
