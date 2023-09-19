from fastapi import APIRouter
import json

router = APIRouter()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

compteur_afficher_donnees = 0


@router.get('/')
async def afficher_donnees():
    """
    Cette fonction permet d'afficher toutes les dates présentes dans le fichier JSON.

    Returns:
        dict: Le nombre de requêtes pour afficher les données et les données météorologiques.
    """
    global compteur_afficher_donnees
    compteur_afficher_donnees += 1
    return {"nombre_requetes_donnees": compteur_afficher_donnees, "weather_data": weather_data}
