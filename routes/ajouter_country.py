import mysql.connector
from fastapi import APIRouter, HTTPException

from mysql_connection import config

router = APIRouter()


@router.post('/{country}')
async def ajouter_country(country: str):
    """
    Ajoute des données météorologiques pour un pays spécifique à la base de données.

    Args:
        country (str): Le nom du pays à ajouter.

    Returns:
        dict: Un dictionnaire contenant les informations suivantes :
            - {"ajouter_country": "Ajout effectué"} en cas de succès.

    Raises:
        HTTPException (500): Si une erreur de base de données se produit.
    """

    try:
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "INSERT INTO country (name) VALUES (%s)"
                c.execute(query, (country,))
                db.commit()

        return {"ajouter_country": 'Ajout effectué'}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
