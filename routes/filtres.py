from fastapi import APIRouter, HTTPException
import json

router = APIRouter()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

compteur_filtrer_date = 0
compteur_filtrer_temp = 0
compteur_filtrer_country = 0
compteur_filtrer_city = 0

compteur_dates = {}
compteur_temp = {}
compteur_country = {}
compteur_city = {}

@router.get('/date/{annee}-{mois}-{jour}')
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

@router.get('/temp/{args}')
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

    temp = []
    for data in weather_data:
        if data['tmax'] == args:
            temp.append(data)
    return {"nombre_requetes_filtrer_temp": compteur_filtrer_temp,
            "nombre_requetes_date_specifique": compteur_temp[args], "weather_data": temp}

@router.get('/country/{countries}')
async def filtrer_country(countries: str):
    global compteur_filtrer_country
    compteur_filtrer_country += 1

    # Incrémente le compteur pour ce pays spécifique
    compteur_country[countries] = compteur_country.get(countries, 0) + 1

    countries_data = []
    for data in weather_data:
        if data['country'] == countries:
            countries_data.append(data)

    return countries_data
