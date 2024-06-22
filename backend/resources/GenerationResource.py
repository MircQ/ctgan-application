import io
from fastapi import APIRouter
from starlette.responses import Response
from services.ModelService import ModelService

generation_router = APIRouter(
    tags=["Generation"]
)


@generation_router.get(
    path="/generate",
    summary="Generate new samples",
    description="Generate new samples from th current model."
)
def generate(samples: int) -> Response:

    synthetic_data = ModelService().generate(samples=samples)

    buffer = io.BytesIO()

    # Writing dataframe into the buffer
    synthetic_data.to_csv(path_or_buf=buffer, index=False)
    
    # Set buffer cursor to the initial position
    buffer.seek(0)

    return Response(
        content=buffer.read(),
        media_type="text/csv",
        headers={'Content-Disposition': 'attachment; filename="samples.csv"'}
    )
