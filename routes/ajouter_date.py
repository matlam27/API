import mysql.connector
from fastapi import APIRouter, HTTPException

from database import config

router = APIRouter()

compteur_par_date = 0
compteur_par_date_specifique = {}

@router.post('/{annee}-{mois}-{jour}/{tmin}/{tmax}/{prcp}/{snow}/{swnd}/{awnd}/{country}/{city}')
async def ajouter_date(annee: str, mois: str, jour: str, tmin: int, tmax: int, prcp: float, snow: float, swnd: float, awnd: float, country: str, city: str):
    """
    Ajoute des données météorologiques pour une date spécifique à la base de données.

    Args:
        annee (str): L'année de la date au format 'AAAA'.
        mois (str): Le mois de la date au format 'MM'.
        jour (str): Le jour de la date au format 'JJ'.
        tmin (int): La température minimale.
        tmax (int): La température maximale.
        prcp (float): La précipitation.
        snow (float): L'accumulation de neige.
        swnd (float): La vitesse du vent au sol.
        awnd (float): La vitesse moyenne du vent.
        country (str): Le pays.
        city (str): La ville.

    Returns:
        dict: Un dictionnaire contenant les informations suivantes :
            - {"ajouter_date": "Sauvegarde effectuée"} en cas de succès.
            - {"nombre_requetes_par_date": compteur_par_date, "nombre_requetes_par_date_specifique": compteur_par_date_specifique} pour le suivi du nombre de requêtes par date.

    Raises:
        HTTPException (500): Si une erreur de base de données se produit.
    """
    try:
        global compteur_par_date
        compteur_par_date += 1

        date = f"{annee}-{mois}-{jour}"

        compteur_par_date_specifique[date] = compteur_par_date_specifique.get(date, 0) + 1

        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "INSERT INTO meteo (date, tmin, tmax, prcp, snow, swnd, awnd, country, city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                c.execute(query, (date, tmin, tmax, prcp, snow, swnd, awnd, country, city))
                result = c.fetchall()

                return {"ajouter_date": 'Sauvegarde effectué',
                        "nombre_requetes_par_date": compteur_par_date, "nombre_requetes_par_date_specifique": compteur_par_date_specifique}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
