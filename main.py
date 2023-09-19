from fastapi import FastAPI
from datetime import datetime
import json

app = FastAPI()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

@app.get('/date')
async def afficher_date():
    """
    Cette fonction permet d'afficher toutes les dates présentes dans le fichier json.
    """
    return weather_data

@app.get('/date/{id}')
async def filtre_date(id : int):
    """
    Cette fonction permet de filtrer les données par date.
    Args:
        params : id de recherche.
    Returns:
        la date en fonction de l'id.
    """
    weather_data_id = weather_data[id]
    return weather_data_id


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
