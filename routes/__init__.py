from fastapi import APIRouter
from . import afficher_donnees, ajouter_date, ajouter_city, ajouter_country, filtre_date, filtre_tmax, filtre_tmin, filter_precipitation, supprimer_date, update, filter_country, filter_city

router = APIRouter()

router.include_router(afficher_donnees.router)
router.include_router(ajouter_date.router, prefix="/ajouter_date")
router.include_router(ajouter_city.router, prefix="/ajouter_city")
router.include_router(ajouter_country.router, prefix="/ajouter_country")
router.include_router(filtre_date.router, prefix="/date")
router.include_router(filtre_tmax.router, prefix="/tmax")
router.include_router(filtre_tmin.router, prefix="/tmin")
router.include_router(filter_precipitation.router, prefix="/precipitation")
router.include_router(filter_country.router, prefix="/country")
router.include_router(filter_city.router, prefix="/city")
router.include_router(supprimer_date.router, prefix="/delete")
router.include_router(update.router, prefix="/update")
