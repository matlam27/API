from fastapi import APIRouter
from . import afficher_meteo, afficher_city, afficher_country, ajouter_date, filtre_date, filtre_tmax, filtre_tmin, filter_precipitation, supprimer_date, supprimer_country, supprimer_city, update_meteo, update_country, update_city, filter_country, filter_city, ajouter_city, ajouter_country, filter_country, filter_city

router = APIRouter()

# POST methods
router.include_router(ajouter_date.router, prefix="/weather")
router.include_router(ajouter_city.router, prefix="/city")
router.include_router(ajouter_country.router, prefix="/country")

# GET methods
router.include_router(afficher_meteo.router)
router.include_router(afficher_city.router, prefix="/weather")
router.include_router(afficher_country.router, prefix="/weather")
router.include_router(filtre_date.router, prefix="/weather")
router.include_router(filtre_tmax.router, prefix="/tmax")
router.include_router(filtre_tmin.router, prefix="/tmin")
router.include_router(filter_precipitation.router, prefix="/prcp")
router.include_router(filter_city.router, prefix="/city")
router.include_router(filter_country.router, prefix="/country")

# DELETE methods
router.include_router(supprimer_date.router, prefix="/weather")
router.include_router(supprimer_country.router, prefix="/country")
router.include_router(supprimer_city.router, prefix="/city")

# PUT methods
router.include_router(update_meteo.router, prefix="/weather")
router.include_router(update_country.router, prefix="/country")
router.include_router(update_city.router, prefix="/city")