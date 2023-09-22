import mysql.connector
from fastapi import APIRouter, HTTPException
from database import config
from pydantic import BaseModel

router = APIRouter()


class WeatherData(BaseModel):
    date: str
    tmin: int
    tmax: int
    prcp: float
    snow: float
    snwd: float
    awnd: float
    id_city: int


@router.put('/{date}')
async def update_date(date: str, weather_data: WeatherData):
    tmin = weather_data.tmin
    tmax = weather_data.tmax
    prcp = weather_data.prcp
    snow = weather_data.snow
    snwd = weather_data.snwd
    awnd = weather_data.awnd
    id_city = weather_data.id_city

    try:
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = """
                    UPDATE meteo
                    SET tmin = %s, tmax = %s, prcp = %s, snow = %s, snwd = %s, awnd = %s, id_city = %s
                    WHERE date = %s
                """
                c.execute(query, (tmin, tmax, prcp, snow,
                          snwd, awnd, id_city, date))
                db.commit()

                if c.rowcount > 0:
                    return {"la mise à jour a été effectuée"}
                else:
                    return "la date est introuvable"

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
