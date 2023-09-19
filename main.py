from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

compteur_afficher_donnees = 0
compteur_ajouter_date = 0
compteur_filtrer_date = 0
compteur_filtrer_temp = 0
compteur_filtrer_prcp = 0
compteur_delete = 0

# Dictionnaire pour stocker le nombre de requêtes pour chaque date, température et precipitation
compteur_dates = {}
compteur_temp = {}
compteur_prcp = {}

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
    """
    Cette fonction permet d'afficher toutes les dates présentes dans le fichier JSON.

    Returns:
        dict: Le nombre de requêtes pour afficher les données et les données météorologiques.
    """
    global compteur_afficher_donnees
    compteur_afficher_donnees += 1
    return {"nombre_requetes_donnees": compteur_afficher_donnees, "weather_data": weather_data}

@app.get('/ajouter-date/{date}/{tmin}/{tmax}/{prcp}/{snow}/{snwd}/{awnd}')
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
            raise HTTPException(status_code=400, detail="La date existe déjà dans le fichier JSON")

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

@app.get('/filter/date/{annee}-{mois}-{jour}')
async def filtrer_date(annee, mois, jour):
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
    global compteur_filtrer_date
    compteur_filtrer_date += 1

    date = (f'{annee}-{mois}-{jour}')

    # Incrémente le compteur pour cette date spécifique
    compteur_dates[date] = compteur_dates.get(date, 0) + 1

    for data in weather_data:
        if data['date'] == date:
            return {"nombre_requetes_filtrer_date": compteur_filtrer_date,
                    "nombre_requetes_date_specifique": compteur_dates[date], "weather_data": data}

    raise HTTPException(status_code=404, detail="Date introuvable dans le fichier JSON")

@app.get('/filter/temp/{args}')
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
        http://127.0.0.1:8000/filter/temp/82
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

@app.get('/date/precipitation/{prcp}')
async def precipitation_date(prcp: float):
    """
    Cette fonction permet d'afficher les dates ayant une précipitation égale à la valeur spécifiée.

    Args:
        prcp (float): La valeur de précipitation à utiliser comme critère de filtrage.

    Returns:
        list: Une liste des dates ayant une précipitation égale à la valeur spécifiée.

    Example:
        Pour obtenir les dates avec une précipitation de 0.62, vous pouvez accéder à cette URL avec une requête GET :
        http://127.0.0.1:8000/date/precipitation/0.62
    """
    global compteur_filtrer_prcp
    compteur_filtrer_prcp += 1

    # Incrémente le compteur pour cette précipitation spécifique
    compteur_prcp[prcp] = compteur_prcp.get(prcp, 0) + 1

    date = prcp
    precipitation_tab = []
    for precipitation in weather_data:
        if precipitation['prcp'] == date:
            precipitation_tab.append(precipitation)

    return {"nombre_requetes_filtrer_prcp": compteur_filtrer_prcp,
            "nombre_requetes_prcp_specifique": compteur_prcp[prcp], "precipitation_tab": precipitation_tab}


@app.delete('/delete/{annee}-{mois}-{jour}')
async def supprimer_date(annee, mois, jour):
    """
    Supprime une date du fichier JSON.

    Args:
        annee (str): L'année de la date à supprimer.
        mois (str): Le mois de la date à supprimer.
        jour (str): Le jour de la date à supprimer.

    Returns:
        dict: Un dictionnaire contenant un message indiquant que la date a été supprimée avec succès.

    Raises:
        HTTPException: Une exception HTTP 404 est levée si la date n'a pas été trouvée dans les données.

    Example:
        Pour supprimer la date '2023-09-19', vous pouvez accéder à cette URL avec une requête DELETE :
        http://127.0.0.1:8000/delete/2023-09-19
    """
    global compteur_delete
    compteur_delete += 1

    global weather_data

    date_to_delete =  f'{annee}-{mois}-{jour}'

    for i, data in enumerate(weather_data):
        if data['date'] == date_to_delete:
            del weather_data[i]
            with open("rdu-weather-history.json", "w") as json_file:
                json.dump(weather_data, json_file)
            return {"message": "Date supprimée avec succès", "compteur_delete": compteur_delete}

    raise HTTPException(
        status_code=404, detail="la date est introuvable")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
