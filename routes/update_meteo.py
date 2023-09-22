from fastapi import APIRouter, HTTPException
from database import config
import mysql.connector

router = APIRouter()

@router.put('/{id}')
async def update_meteo(id: int, data: dict):
    """
    Mettre à jour les données météorologiques d'une entrée existante dans la base de données.

    Paramètres :
    - id (int) : L'identifiant de l'entrée à mettre à jour.
    - data (dict) : Un dictionnaire contenant les données à mettre à jour, y compris :
      - "date" (str) : La date des données météorologiques.
      - "tmin" (float) : La température minimale.
      - "tmax" (float) : La température maximale.
      - "prcp" (float) : Les précipitations.
      - "snow" (float) : La neige.
      - "snwd" (float) : L'accumulation de neige au sol.
      - "awnd" (float) : La vitesse moyenne du vent.
      - "id_city" (int) : L'identifiant de la ville associée aux données.

    Retours :
    - dict : Un message indiquant si les données ont été mises à jour avec succès ou si aucune donnée n'a été mise à jour.

    Exceptions :
    - HTTPException : En cas d'erreur de base de données, une exception HTTP avec un code d'état 500 est levée, et les détails de l'erreur sont inclus dans le message.

    Remarque :
    Cette route permet de mettre à jour les données météorologiques d'une entrée existante dans la base de données en spécifiant les champs à mettre à jour dans le dictionnaire 'data'. Si un champ est laissé vide ou à 'None', il ne sera pas mis à jour.
    """
    try:
        date = data.get("date")
        tmin = data.get("tmin")
        tmax = data.get("tmax")
        prcp = data.get("prcp")
        snow = data.get("snow")
        snwd = data.get("snwd")
        awnd = data.get("awnd")
        id_city = data.get("id_city")

        with mysql.connector.connect(**config) as db:
            with db.cursor() as c:
                c.execute("SELECT * FROM meteo WHERE id = %s", (id,))
                existing_data = c.fetchone()

                if existing_data:
                    update_fields = []
                    update_values = []

                    if date:
                        update_fields.append("date = %s")
                        update_values.append(date)
                    if tmin is not None:
                        update_fields.append("tmin = %s")
                        update_values.append(tmin)
                    if tmax is not None:
                        update_fields.append("tmax = %s")
                        update_values.append(tmax)
                    if prcp is not None:
                        update_fields.append("prcp = %s")
                        update_values.append(prcp)
                    if snow is not None:
                        update_fields.append("snow = %s")
                        update_values.append(snow)
                    if snwd is not None:
                        update_fields.append("snwd = %s")
                        update_values.append(snwd)
                    if awnd is not None:
                        update_fields.append("awnd = %s")
                        update_values.append(awnd)
                    if id_city is not None:
                        update_fields.append("id_city = %s")
                        update_values.append(id_city)

                    if update_fields:
                        query = f"UPDATE meteo SET {', '.join(update_fields)} WHERE id = %s"
                        update_values.append(id)
                        c.execute(query, tuple(update_values))
                        db.commit()
                        return {"message": "Données mises à jour avec succès"}
                    else:
                        return {"message": "Aucune donnée à mettre à jour"}

                else:
                    return 'ID introuvable dans la base de données.'

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erreur de base de données : {err}")
