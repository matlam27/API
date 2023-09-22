import decimal

import mysql.connector
from fastapi import APIRouter, HTTPException
from mysql_connection import config

router = APIRouter()

@router.get('/{prcp}')
async def precipitation_date(prcp: float):
    """
        Récupère les données de précipitations depuis la base de données en fonction d'une valeur de précipitations donnée.

        Args:
            prcp (float): La valeur de précipitations à rechercher.

        Returns:
            dict: Un dictionnaire contenant les données de précipitations.

        Raises:
            HTTPException: Levée avec un code d'état 404 si aucune donnée n'est trouvée, ou avec un code d'état 500 en cas d'erreur de la base de données.
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