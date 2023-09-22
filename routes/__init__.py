from fastapi import APIRouter
from . import afficher_donnees, ajouter_date, filtre_date, filtre_tmax, filtre_tmin, precipitation_date, supprimer_date, update, filter_country, filter_city, ajouter_city, ajouter_country

router = APIRouter()

router.include_router(afficher_donnees.router)
router.include_router(ajouter_date.router, prefix="/add-date")
router.include_router(filtre_date.router, prefix="/search-by-date")
router.include_router(filtre_tmax.router, prefix="/search-by-tmax")
router.include_router(filtre_tmin.router, prefix="/search-by-tmin")
router.include_router(precipitation_date.router, prefix="/search-by-prcp")
router.include_router(supprimer_date.router, prefix="/remove-date")
router.include_router(update.router, prefix="/update-date")
router.include_router(filter_country.router, prefix="/search-by-country")
router.include_router(filter_city.router, prefix="/search-by-city")
router.include_router(ajouter_city.router, prefix="/add_city")
router.include_router(ajouter_country.router, prefix="/add_country")