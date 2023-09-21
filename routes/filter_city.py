import mysql.connector
from fastapi import APIRouter, HTTPException, Query

from database import config

router = APIRouter()

compteur_par_ville = 0
compteur_par_ville_specifique = {}

@router.get('/{city}')
async def city_date(city: str):
    """
    Récupère les données météorologiques pour une ville spécifique depuis la base de données.

    Args:
        city (str): Le nom de la ville pour laquelle vous souhaitez récupérer les données météorologiques.

    Returns:
        dict: Un dictionnaire contenant les informations suivantes :
            - {"city_data": data, "nombre_requetes_par_ville": compteur_par_ville, "nombre_requetes_par_ville_specifique": compteur_par_ville_specifique} en cas de succès.

    Raises:
        HTTPException (404): Si aucune donnée n'est trouvée pour la ville spécifiée.
        HTTPException (500): Si une erreur de base de données se produit.
    """
    try:
        global compteur_par_ville
        compteur_par_ville += 1

        compteur_par_ville_specifique[city] = compteur_par_ville_specifique.get(city, 0) + 1

        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "SELECT * FROM meteo WHERE city = %s"
                c.execute(query, (city,))
                result = c.fetchall()

                if not result:
                    raise HTTPException(status_code=404, detail="Data not found")

                # Convert the result to a list of dictionaries
                data = [dict(zip(c.column_names, row)) for row in result]

                return {"city_data": data,
                        "nombre_requetes_par_ville": compteur_par_ville, "nombre_requetes_par_ville_specifique": compteur_par_ville_specifique}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
