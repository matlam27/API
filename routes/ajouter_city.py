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
                c.execute("SELECT * FROM city WHERE name = %s", (city,))
                existing_city = c.fetchone()

                if existing_city:
                    return {"ajouter_country": "Ville déjà existante"}
                else:
                    query = "INSERT INTO city (name, id_country) VALUES (%s, %s)"
                    c.execute(query, (city,id_country,))
                    db.commit()

        return {"ajouter_city": 'Ajout effectué'}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")