import mysql.connector
from fastapi import APIRouter, HTTPException
from database import config

router = APIRouter()

@router.get('/{prcp}')
async def filter_precipitation(prcp: float):
    """
    Récupère et affiche les données météorologiques filtrées par précipitation.

    Paramètres :
        prcp (float) : La valeur de précipitation pour filtrer les données météorologiques.

    Retours :
        dict : Un dictionnaire contenant les données météorologiques filtrées par précipitation.

    Erreurs HTTP possibles :
        - HTTP 500: En cas d'erreur de base de données.
        - HTTP 404: Si aucune donnée n'est trouvée dans la table 'meteo' pour la valeur de précipitation spécifiée.

    Raises:
        HTTPException: Si une erreur de base de données se produit, une exception HTTP avec un code d'état 500 est levée, et les détails de l'erreur sont inclus dans le message.

    Exemple :
        Pour récupérer les données météorologiques avec une valeur de précipitation de 0.5, envoyez une requête GET à cette URL : '/{prcp}'.
    """
    try:
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "SELECT * FROM meteo WHERE prcp = %s"
                c.execute(query, (prcp,))
                result = c.fetchall()

                if not result:
                    raise HTTPException(status_code=404, detail="Data not found")

                data = [dict(zip(c.column_names, row)) for row in result]

                return {"prcp_data": data}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")