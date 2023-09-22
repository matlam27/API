from fastapi import APIRouter, HTTPException
from database import config
import mysql.connector

router = APIRouter()

@router.put('/{id}')
async def update_country(id: int, data: dict):
    """
    Mettre à jour le nom d'un pays existant dans la base de données.

    Paramètres :
    - id (int) : L'identifiant du pays à mettre à jour.
    - data (dict) : Un dictionnaire contenant les données à mettre à jour, y compris :
      - "name" (str) : Le nouveau nom du pays.

    Retours :
    - dict : Un message indiquant si le nom du pays a été mis à jour avec succès ou si aucune donnée n'a été mise à jour.

    Exceptions :
    - HTTPException : En cas d'erreur de base de données, une exception HTTP avec un code d'état 500 est levée, et les détails de l'erreur sont inclus dans le message.

    Remarque :
    Cette route permet de mettre à jour le nom d'un pays existant dans la base de données en spécifiant le nouveau nom dans le dictionnaire 'data'.
    """
    try:
        name = data.get("name")

        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                c.execute("SELECT * FROM country WHERE id = %s", (id,))
                existing_country = c.fetchone()

                if existing_country:
                    if name:
                        c.execute("UPDATE country SET name = %s WHERE id = %s", (name, id))
                        db.commit()
                        return {"message": "Nom du pays mis à jour avec succès"}
                    else:
                        return {"message": "Le nouveau nom du pays est vide, aucune mise à jour effectuée."}

                else:
                    return 'ID introuvable dans la base de données.'

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erreur de base de données : {err}")
