import mysql.connector
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from mysql_connection import config

router = APIRouter()

compteur_par_date = 0
compteur_par_date_specifique = {}


@router.post('/{city}/{id_country}')
async def ajouter_city(city: str, id_country: int):
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
                query = "INSERT INTO city (name, id_country) VALUES (%s, %s)"
                c.execute(query, (city,id_country,))
                db.commit()

        return {"ajouter_city": 'Ajout effectué'}

    except mysql.connector.Error as err:
        # Gérer les erreurs de base de données
        raise HTTPException(status_code=500, detail=f"Database error: {err}")