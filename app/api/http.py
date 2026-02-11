from fastapi import APIRouter

from domain.models.plant import Plant
from domain.types import PlantSettings

# import httpx
# from clients.constants import OPENAI_API_KEY
# from fastapi.responses import JSONResponse


def create_plant_router(plant: Plant):
    router = APIRouter()

    @router.get("/get-plant-settings")
    async def get_plant_settings():
        return plant.get_plant_settings()

    @router.get("/get-plant-states")
    async def get_plant_states():
        return plant.get_states()

    @router.post("/update-plant-settings")
    async def update_plant_settings(settings: PlantSettings):
        plant.name = settings.name
        plant.type = settings.type.value
        plant.voice = settings.voice.value
        plant.sassiness = settings.sassiness.value
        return {"message": "plant settings successfully updated"}

    # # get an ephemeral key for FE to communicate with openai websocket
    # # currently unused, keeping just in case
    # @router.post("/session")
    # async def get_ephemeral_key():
    #     try:
    #         async with httpx.AsyncClient(timeout=30.0) as client:
    #             response = await client.post(
    #                 "https://api.openai.com/v1/realtime/sessions",
    #                 headers={
    #                     "Authorization": f"Bearer {OPENAI_API_KEY}",
    #                     "Content-Type": "application/json",
    #                 },
    #                 json={
    #                     "model": "gpt-realtime",
    #                     "modalities": ["audio", "text"],
    #                     "instructions": (
    #                         "You are a dramatic, slightly judgmental but lovable house plant. "
    #                         "You give sassy commentary while still being helpful."
    #                     ),
    #                 },
    #             )

    #         if response.status_code != 200:
    #             print("error")

    #         return JSONResponse(response.json())

    #     except httpx.RequestError as e:
    #         print("error", e)

    #     except Exception as e:
    #         print("error,", e)

    return router
