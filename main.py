from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

compteur_afficher_donnees = 0
compteur_ajouter_date = 0
compteur_filtrer_date = 0

# Dictionnaire pour stocker le nombre de requêtes pour chaque date
compteur_dates = {}


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
    """Cette fonction permet d'afficher toutes les dates présentes dans le fichier JSON."""
    global compteur_afficher_donnees
    compteur_afficher_donnees += 1
    return {"nombre_requetes_donnees": compteur_afficher_donnees, "weather_data": weather_data}


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
    global compteur_ajouter_date
    compteur_ajouter_date += 1

    if date_to_add in weather_data:
        raise HTTPException(
            status_code=400, detail="La date existe déjà dans le fichier JSON")

    weather_data.append(date_to_add)

    with open('rdu-weather-history.json', 'w') as json_file:
        json.dump(weather_data, json_file, indent=4)

    return {"message": "Date ajoutée avec succès", "compteur_ajouter_date": compteur_ajouter_date}


@app.get('/filter/date/{annee}-{mois}-{jour}')
async def filtrer_date(annee, mois, jour):
    """
    Affiche les données pour une date spécifique.

    Args:
        annee (int): L'année de la date à afficher.
        mois (int): Le mois de la date à afficher.
        jour (int): Le jour de la date à afficher.

    Returns:
        dict: Les données de la date demandée.

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

    raise HTTPException(
        status_code=404, detail="Date introuvable dans le fichier JSON")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


@app.delete('/date/{annee}-{mois}-{jour}')
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

    """
    global weather_data

    date_to_delete = f'{annee}-{mois}-{jour}'

    for i, data in enumerate(weather_data):
        if data['date'] == date_to_delete:
            del weather_data[i]
            with open("rdu-weather-history.json", "w") as json_file:
                json.dump(weather_data, json_file)
            return {"la date a été supprimée avec succès"}

    raise HTTPException(
        status_code=404, detail="la date est introuvable")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
