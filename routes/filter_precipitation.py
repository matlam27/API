import mysql.connector
from fastapi import APIRouter, HTTPException, Query

from database import config

router = APIRouter()

compteur_par_precipitation = 0
compteur_par_precipitation_specifique = {}

@router.get('/{prcp}')
async def country_date(prcp: float):
    """
    Récupère les données météorologiques pour une valeur de précipitation spécifique depuis la base de données.

    Args:
        prcp (float): La valeur de précipitation pour laquelle vous souhaitez récupérer les données météorologiques.

    Returns:
        dict: Un dictionnaire contenant les informations suivantes :
            - {"country_data": data, "nombre_requetes_par_precipitation": compteur_par_precipitation, "nombre_requetes_par_precipitation_specifique": compteur_par_precipitation_specifique} en cas de succès.

    Raises:
        HTTPException (404): Si aucune donnée n'est trouvée pour la valeur de précipitation spécifiée.
        HTTPException (500): Si une erreur de base de données se produit.
    """
    try:
        global compteur_par_precipitation
        compteur_par_precipitation += 1

        compteur_par_precipitation_specifique[prcp] = compteur_par_precipitation_specifique.get(prcp, 0) + 1

        # Se connecter à la base de données
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                # Construire et exécuter la requête SQL avec un paramètre
                query = "SELECT * FROM meteo WHERE prcp = %s"
                c.execute(query, (prcp,))
                result = c.fetchall()

                # Vérifier si des résultats ont été trouvés
                if not result:
                    raise HTTPException(status_code=404, detail="Data not found")

                # Convertir le résultat en une liste de dictionnaires
                data = [dict(zip(c.column_names, row)) for row in result]

                return {"country_data": data,
                        "nombre_requetes_par_precipitation": compteur_par_precipitation, "nombre_requetes_par_precipitation_specifique": compteur_par_precipitation_specifique}

    except mysql.connector.Error as err:
        # Gérer les erreurs de base de données
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
