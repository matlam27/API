from fastapi import FastAPI
import json

app = FastAPI()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

@app.get('/update/{annee}-{mois}-{jour}/{args}/{modification}')
async def update(annee, mois, jour, args, modification):
    date = f'{annee}-{mois}-{jour}'
    if args != 'date':
        modification = int(modification)
    for data in weather_data:
        if data['date'] == date:
            data[args] = modification
            return data
    return 'Date introuvable. Veuillez indiquer une date dans le format : annee-mois-jour.'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)