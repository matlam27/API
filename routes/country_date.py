import mysql.connector
from fastapi import APIRouter, HTTPException, Query

from mysql_connection import config

router = APIRouter()


@router.get('/{country}')
async def country_date(country: str):
    try:
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

                return {"country_data": data}

    except mysql.connector.Error as err:
        # Handle database errors
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
