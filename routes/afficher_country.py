import mysql
from fastapi import APIRouter, HTTPException

from database import config

router = APIRouter()

compteur_afficher_country = 0

@router.get('/')
async def afficher_country():
    """
    Récupère et affiche les données de la table 'country'.

    Retours :
        dict : Un dictionnaire contenant les données de la table 'country'.

    Erreurs HTTP possibles :
        - HTTP 500: En cas d'erreur de base de données.
        - HTTP 404: Si aucune donnée n'est trouvée dans la table 'country'.

    Raises:
        HTTPException: Si une erreur de base de données se produit, une exception HTTP avec un code d'état 500 est levée, et les détails de l'erreur sont inclus dans le message.

    Exemple :
        Pour récupérer les données de la table 'country', envoyez une requête GET à cette URL.
    """
    try:
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "SELECT * FROM country"
                c.execute(query)
                result = c.fetchall()

                if not result:
                    raise HTTPException(status_code=404, detail="Data not found")

                # Convert the result to a list of dictionaries
                data = [dict(zip(c.column_names, row)) for row in result]

                return {"meteo_data": data}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")