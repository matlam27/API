from fastapi import APIRouter
from . import afficher_donnees, ajouter_date, filtre_date, filtre_tmax, filtre_tmin, precipitation_date, supprimer_date, update, filter_country, filter_city, ajouter_city, ajouter_country

router = APIRouter()

router.include_router(afficher_donnees.router)

# POST methods
router.include_router(ajouter_date.router, prefix="/weather")
router.include_router(ajouter_city.router, prefix="/city")
router.include_router(ajouter_country.router, prefix="/country")

# GET methods
router.include_router(filtre_date.router, prefix="/weather")
router.include_router(filtre_tmax.router, prefix="/tmax")
router.include_router(filtre_tmin.router, prefix="/tmin")
router.include_router(precipitation_date.router, prefix="/prcp")
router.include_router(filter_city.router, prefix="/city")
router.include_router(filter_country.router, prefix="/country")

# DELETE methods
router.include_router(supprimer_date.router, prefix="/weather")

# PATCH methods
router.include_router(update.router, prefix="/weather")
