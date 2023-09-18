from fastapi import FastAPI
from datetime import datetime
import json

app = FastAPI()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

@app.get('/meteo')
async def obtenir_meteo(date: str = None):
    if date:
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return {"message": "Format de date invalide. Utilisez YYYY-MM-DD."}, 400
    else:
        date = datetime.now()

    meteo = None
    for entry in weather_data:
        if entry["date"] == date.strftime("%Y-%m-%d"):
            meteo = entry
            break

    if meteo is None:
        return {"message": "Aucune donnée météorologique disponible pour cette date."}, 404

    return meteo

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
