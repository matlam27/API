import mysql.connector
from fastapi import APIRouter, HTTPException, Query

from mysql_connection import config

router = APIRouter()


@router.get('/{city}')
async def city_date(city: str):
    try:
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "SELECT * FROM meteo WHERE city = %s"
                c.execute(query, (city,))
                result = c.fetchall()

                if not result:
                    raise HTTPException(status_code=404, detail="Data not found")

                # Convert the result to a list of dictionaries
                data = [dict(zip(c.column_names, row)) for row in result]

                return {"city_data": data}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")