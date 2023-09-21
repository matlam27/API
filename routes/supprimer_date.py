import mysql.connector
from fastapi import APIRouter, HTTPException
from mysql_connection import config

router = APIRouter()


@router.delete('/{date}')
async def supprimer_date(date: str):
    try:
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "DELETE FROM meteo WHERE date = %s"
                c.execute(query, (date,))
                db.commit()

                if c.rowcount == 0:
                    raise HTTPException(
                        status_code=404, detail="Data not found")

                return {"message": " la date a bien été supprimée"}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
