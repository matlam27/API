import mysql.connector
from fastapi import APIRouter, HTTPException, Query
from mysql_connection import config

router = APIRouter()

@router.get('/{city}/{id_city}')
async def city_date(id_city: int):
    """
    Récupère les données de météo pour une ville spécifiée par son identifiant.

    Args:
        id_city (int): L'identifiant de la ville pour laquelle récupérer les données de météo.

    Returns:
        dict: Un dictionnaire contenant les données de météo pour la ville spécifiée.

    Raises:
        HTTPException: Levée avec un code d'état 404 si aucune donnée n'est trouvée, ou avec un code d'état 500 en cas d'erreur de la base de données.
    """
    try:
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "SELECT meteo.*, city.name AS city_name FROM meteo JOIN city ON meteo.id_city = city.id WHERE meteo.id_city = %s"
                c.execute(query, (id_city, ))
                result = c.fetchall()

                if not result:
                    raise HTTPException(status_code=404, detail="Données non trouvées")

                # Convertir le résultat en une liste de dictionnaires
                data = [dict(zip(c.column_names, row)) for row in result]

                return {"city_data": data}

    except mysql.connector.Error as err:
        # Gérer les erreurs de base de données
        raise HTTPException(status_code=500, detail=f"Erreur de la base de données : {err}")
