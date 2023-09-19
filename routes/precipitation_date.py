from fastapi import APIRouter
import json

router = APIRouter()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

compteur_filtrer_prcp = 0
compteur_prcp = {}


@router.get('/{prcp}')
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
