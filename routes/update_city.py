import mysql.connector
from fastapi import APIRouter, HTTPException

from database import config

router = APIRouter()

@router.put('/{id}')
async def update_country(id: int, data: dict):
    """
    Mettre à jour le nom et l'identifiant d'un pays existant dans la base de données.

    Paramètres :
    - id (int) : L'identifiant du pays à mettre à jour.
    - data (dict) : Un dictionnaire contenant les données à mettre à jour, y compris :
      - "name" (str) : Le nouveau nom du pays.
      - "id_country" (int) : Le nouvel identifiant du pays.

    Retours :
    - dict : Un message indiquant si le nom et l'identifiant du pays ont été mis à jour avec succès ou si aucune donnée n'a été mise à jour.

    Exceptions :
    - HTTPException : En cas d'erreur de base de données, une exception HTTP avec un code d'état 500 est levée, et les détails de l'erreur sont inclus dans le message.

    Remarque :
    Cette route permet de mettre à jour le nom et l'identifiant d'un pays existant dans la base de données en spécifiant les nouvelles valeurs dans le dictionnaire 'data'.
    """
    try:
        name = data.get("name")
        id_country = data.get("id_country")

        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                c.execute("SELECT * FROM city WHERE id = %s", (id,))
                existing_country = c.fetchone()

                if existing_country:
                    update_fields = []
                    update_values = []

                    if name:
                        update_fields.append("name = %s")
                        update_values.append(name)
                    if id_country:
                        update_fields.append("id_country = %s")
                        update_values.append(id_country)

                    if update_fields:
                        update_values.append(id)
                        query = f"UPDATE city SET {', '.join(update_fields)} WHERE id = %s"
                        c.execute(query, tuple(update_values))
                        db.commit()
                        return {"message": "Nom et identifiant du pays mis à jour avec succès"}
                    else:
                        return {"message": "Aucune donnée à mettre à jour"}

                else:
                    return 'ID introuvable dans la base de données.'

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erreur de base de données : {err}")
