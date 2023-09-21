import mysql
from fastapi import APIRouter, HTTPException
import json

from database import config

router = APIRouter()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

compteur_afficher_donnees = 0

@router.get('/')
async def afficher_donnees_date():
    """
    Récupère les données météorologiques depuis la base de données.

    Returns:
        dict: Un dictionnaire contenant les données météorologiques.
        - {"meteo_data": data, "nombre_requetes_afficher_donnees": compteur_afficher_donnees}

    Raises:
        HTTPException (404): Si aucune donnée n'est trouvée dans la base de données.
        HTTPException (500): Si une erreur de base de données survient.
    """
    try:
        global compteur_afficher_donnees
        compteur_afficher_donnees += 1

        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "SELECT * FROM meteo"
                c.execute(query)
                result = c.fetchall()

                if not result:
                    raise HTTPException(status_code=404, detail="Data not found")

                # Convertir le résultat en une liste de dictionnaires
                data = [dict(zip(c.column_names, row)) for row in result]

                return {"meteo_data": data, "nombre_requetes_afficher_donnees": compteur_afficher_donnees}

    except mysql.connector.Error as err:
        # Gérer les erreurs de base de données
        raise HTTPException(status_code=500, detail=f"Database error: {err}")