import mysql.connector
from fastapi import APIRouter, HTTPException, Query

from database import config

router = APIRouter()

compteur_par_pays = 0
compteur_par_pays_specifique = {}

@router.get('/{country}')
async def country_date(country: str):
    """
    Récupère les données météorologiques pour un pays spécifique depuis la base de données.

    Args:
        country (str): Le nom du pays pour lequel vous souhaitez récupérer les données météorologiques.

    Returns:
        dict: Un dictionnaire contenant les informations suivantes :
            - {"country_data": data, "nombre_requetes_par_pays": compteur_par_pays, "nombre_requetes_par_pays_specifique": compteur_par_pays_specifique} en cas de succès.

    Raises:
        HTTPException (404): Si aucune donnée n'est trouvée pour le pays spécifié.
        HTTPException (500): Si une erreur de base de données se produit.
    """
    try:
        global compteur_par_pays
        compteur_par_pays += 1

        compteur_par_pays_specifique[country] = compteur_par_pays_specifique.get(country, 0) + 1

        # Connect to the database
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                # Build and execute the SQL query with a parameter
                query = "SELECT * FROM meteo WHERE country = %s"
                c.execute(query, (country,))
                result = c.fetchall()

                # Check if any results were found
                if not result:
                    raise HTTPException(status_code=404, detail="Data not found")

                # Convert the result to a list of dictionaries
                data = [dict(zip(c.column_names, row)) for row in result]

                return {"country_data": data,
                        "nombre_requetes_par_pays": compteur_par_pays, "nombre_requetes_par_pays_specifique": compteur_par_pays_specifique}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
