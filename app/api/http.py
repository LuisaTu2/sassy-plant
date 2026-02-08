from fastapi import APIRouter

from domain.models.plant import Plant
from domain.types import PlantSettings


def create_plant_router(plant: Plant):
    router = APIRouter()

    @router.get("/get-plant-settings")
    async def get_plant_settings():
        return plant.get_plant_settings()

    @router.post("/update-plant-settings")
    async def update_plant_settings(settings: PlantSettings):
        plant.name = settings.name
        plant.type = settings.type.value
        plant.voice = settings.voice.value
        plant.sassiness = settings.sassiness.value
        return {"message": "plant settings successfully updated"}

    return router
