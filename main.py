from fastapi import FastAPI
from datetime import datetime
import json

app = FastAPI()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

@app.get('/date')
async def afficher_date():
    """Cette fonction permet d'afficher toutes les dates présentes dans le fichier json."""
    return weather_data

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
