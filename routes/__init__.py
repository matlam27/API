from fastapi import APIRouter
from . import afficher_donnees, ajouter_date, filtres, precipitation_date, supprimer_date, update

router = APIRouter()

router.include_router(afficher_donnees.router, prefix="/donnees")
router.include_router(ajouter_date.router, prefix="/ajouter_date")
router.include_router(filtres.router, prefix="/filter")
router.include_router(precipitation_date.router, prefix="/precipitation")
router.include_router(supprimer_date.router, prefix="/delete")
router.include_router(update.router, prefix="/update")
