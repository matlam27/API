from fastapi import APIRouter, HTTPException
import json

router = APIRouter()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

compteur_delete = 0


@router.delete('/{annee}-{mois}-{jour}')
async def supprimer_date(annee, mois, jour):
    """
    Supprime une date de la BDD.

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