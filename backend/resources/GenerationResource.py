import io

from fastapi import APIRouter
from starlette.responses import Response

from services.ModelService import ModelService

router = APIRouter(
    tags=["Generation"]
)


@router.post(
    path="/generate",
    summary="Generate new samples",
    description="Generate new samples from th current model."
)
def generate(samples: int):

    synthetic_data = ModelService().generate(samples=samples)

    buffer = io.BytesIO()

    synthetic_data.to_csv(path_or_buf=buffer)

    return Response(content=buffer)
