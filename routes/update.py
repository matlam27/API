from fastapi import APIRouter, HTTPException
import json

router = APIRouter()

with open('rdu-weather-history.json', 'r') as json_file:
    weather_data = json.load(json_file)

@router.get('/{annee}-{mois}-{jour}/{args}/{modification}')
async def update(annee, mois, jour, args, modification):
    """
    Met à jour les données météorologiques pour une date spécifique.

    Args:
        annee (str): L'année de la date à mettre à jour.
        mois (str): Le mois de la date à mettre à jour.
        jour (str): Le jour de la date à mettre à jour.
        args (str): Le champ des données météorologiques à mettre à jour.
        modification (str ou int): La nouvelle valeur à attribuer au champ spécifié.

    Returns:
        dict or str: Un dictionnaire contenant les données mises à jour si la date est trouvée,
                     ou une chaîne de caractères indiquant que la date est introuvable.

    Remarques:
        - Si 'args' n'est pas égal à 'date', 'modification' doit être un entier.
        - Le format de la date doit être : 'annee-mois-jour'.
    """
    date = f'{annee}-{mois}-{jour}'
    if args != 'date':
        modification = int(modification)
    for data in weather_data:
        if data['date'] == date:
            data[args] = modification
            return data
    return 'Date introuvable. Veuillez indiquer une date dans le format : annee-mois-jour.'