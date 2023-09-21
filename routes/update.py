from fastapi import APIRouter, HTTPException
from database import config
import mysql.connector

router = APIRouter()

compteur_update = 0
compteur_update_specifique = {}

@router.put('/{annee}-{mois}-{jour}/{args}/{modification}')
async def update(annee: str, mois: str, jour: str, args: str, modification: str):
    """
    Met à jour les données météorologiques pour une date spécifique dans la base de données.

    Args:
        annee (str): L'année de la date à mettre à jour.
        mois (str): Le mois de la date à mettre à jour.
        jour (str): Le jour de la date à mettre à jour.
        args (str): Le champ des données météorologiques à mettre à jour.
        modification (str): La nouvelle valeur à attribuer au champ spécifié.

    Returns:
        dict or str: Un dictionnaire contenant les données mises à jour si la date est trouvée,
                     ou une chaîne de caractères indiquant que la date est introuvable.

    Remarques:
        - Si 'args' n'est pas égal à 'date', 'modification' doit être une chaîne de caractères ou un nombre.
        - Le format de la date doit être : 'annee-mois-jour'.
    """
    global compteur_update
    compteur_update += 1

    date = f'{annee}-{mois}-{jour}'

    compteur_update_specifique[date] = compteur_update_specifique.get(date, 0) + 1

    try:
        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                if args != 'date':
                    modification = int(modification)
                query = f"UPDATE meteo SET {args} = %s WHERE date = %s"
                c.execute(query, (modification, date))
                db.commit()

                if c.rowcount > 0:
                    return {"message": "Données mises à jour avec succès",
                            "compteur_update": compteur_update,
                            "compteur_update_specifique": compteur_update_specifique[date]}
                else:
                    return 'Date introuvable. Veuillez indiquer une date au format : annee-mois-jour.'

    except mysql.connector.Error as err:
        # Gérer les erreurs de base de données
        raise HTTPException(status_code=500, detail=f"Erreur de base de données : {err}")