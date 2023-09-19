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


@app.get('/filter/date/{annee}-{mois}-{jour}')
async def filtrer_date(annee, mois, jour):
    """
    Cette fonction permet d'afficher les données d'une date précise.

    :param annee: L'année de la date à afficher.
    :param mois: Le mois de la date à afficher.
    :param jour: Le jour de la date à afficher.

    Les trois arguments doivent être des nombres entiers.

    :return: Les données de la date demandée.
    """

    date = f'{annee}-{mois}-{jour}'
    for data in weather_data:
        if data['date'] == date:
            return data
    return 'Date introuvable. Veuillez indiquer une date dans le format : annee-mois-jour.'

@app.get('/date/precipitation/{prcp}')
async def precipitation_date(prcp: float):
    """
    Cette fonction permet d'afficher les precipitations des dates.

    Returns:
        date.
    """
    date = prcp
    precipitation_tab = []
    for precipitation in weather_data:
        if precipitation['prcp'] == date:
            precipitation_tab.append(precipitation)

    return precipitation_tab

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
