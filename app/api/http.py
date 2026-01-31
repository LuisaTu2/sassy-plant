from fastapi import APIRouter

from clients.llm_client import llm_client
from domain.types import PlantSettings, current_plant_settings
from domain.utils import temperature_sassiness_mapping

router = APIRouter()


@router.post("/set-plant-settings")
async def set_plant_settings(settings: PlantSettings):
    llm_client.voice = settings.voice.value
    llm_client.temperature = temperature_sassiness_mapping(settings.sassiness.value)
    llm_client.plant_type = settings.plant_type.value
    llm_client.plant_name = settings.name
    current_plant_settings.update(
        {
            "name": settings.name,
            "plant_type": settings.plant_type.value,
            "voice": settings.voice.value,
            "sassiness": settings.sassiness.value,
        }
    )
    # print(
    #     "current plant settings: ",
    #     llm_client.plant_name,
    #     llm_client.voice,
    #     llm_client.temperature,
    #     llm_client.plant_type,
    # )

    return "ok"


# from fastapi import Request
# from fastapi.encoders import jsonable_encoder
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse


# @router.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     # Log the errors to the console/logs
#     print(f"The client sent invalid data in the body: {exc.body}")
#     print(f"Detailed errors: {exc.errors()}")

#     # Return a JSON response to the client
#     return JSONResponse(
#         status_code=422,
#         content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
