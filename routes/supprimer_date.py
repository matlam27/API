import mysql.connector
from fastapi import APIRouter, HTTPException
from database import config

router = APIRouter()

compteur_par_date_supprimer = 0

@router.delete('/{id}')
async def supprimer_date(id: int):
    """
    Supprime les enregistrements de données météorologiques pour une date spécifique de la base de données.

    Args:
        date (str): La date au format 'AAAA-MM-JJ' pour laquelle vous souhaitez supprimer les données météorologiques.

    Returns:
        dict: Un dictionnaire contenant l'un des messages suivants :
            - {"message": "La date a bien été supprimée"} si la suppression est réussie, "nombre_requetes_par_date_supprimer": compteur_par_date_supprimer.
            - Réponse HTTP 404 (Non trouvé) si aucune donnée n'est trouvée pour la date spécifiée.
            - Réponse HTTP 500 (Erreur interne du serveur) si une erreur de base de données se produit.

    Raises:
        HTTPException: En cas d'erreur de base de données, une réponse HTTP avec un code d'erreur 500 sera renvoyée.
    """
    try:
        global compteur_par_date_supprimer
        compteur_par_date_supprimer += 1

        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                query = "DELETE FROM meteo WHERE id = %s"
                c.execute(query, (id,))
                db.commit()

                if c.rowcount == 0:
                    raise HTTPException(
                        status_code=404, detail="Data not found")

                return {"message": "La date a bien été supprimée",
                        "nombre_requetes_par_date_supprimer": compteur_par_date_supprimer,}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")