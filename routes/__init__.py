from fastapi import APIRouter
from . import afficher_donnees, ajouter_date, filter_precipitation, supprimer_date, update, filter_country, filter_city

router = APIRouter()

router.include_router(afficher_donnees.router, prefix="/afficher_donnees")
router.include_router(ajouter_date.router, prefix="/ajouter_date")
router.include_router(supprimer_date.router, prefix="/delete")
router.include_router(update.router, prefix="/update")
router.include_router(filter_precipitation.router, prefix="/prcp")
router.include_router(filter_country.router, prefix="/country")
router.include_router(filter_city.router, prefix="/city")
