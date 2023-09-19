from fastapi import FastAPI
from datetime import datetime
import json

app = FastAPI()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

@app.get('/date')
async def afficher_date():
    return weather_data

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

@app.get('/filter/temp/{args}')
async def filtrer_temp(args):
    args = int(args)
    dates = []
    for data in weather_data:
        if data['tmax'] == args:
            dates.append(data)
    if len(dates) != 0:
        return dates
    return 'Température introuvable. Veuillez indiquer une température en degrés Fahrenheit.'

@app.update('/update/{date}/{args}/{modification}')
async def update(date, args, modification):
    for data in weather_data:
        if data['date'] == date:
            data[args] = modification
            return data
    return 'Date introuvable. Veuillez indiquer une date dans le format : annee-mois-jour.'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)