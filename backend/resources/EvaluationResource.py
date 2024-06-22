import io
from fastapi import APIRouter, UploadFile
import pandas as pd
from starlette.responses import Response
from services.ModelService import ModelService

evaluation_router = APIRouter(
    tags=["Evaluation"]
)


@evaluation_router.post(
    path="/evaluate",
    summary="Evaluate samples",
    description="Evaluate previously computed samples."
)
async def evaluate(column_name: str, synthetic_data_file: UploadFile, real_data_file: UploadFile) -> Response:

    # Reading files as bytes
    synthetic_data_buffer = await synthetic_data_file.read()
    real_data_buffer = await real_data_file.read()

    # Convert into file-like objects
    synthetic_data_b = io.BytesIO(synthetic_data_buffer)
    real_data_b = io.BytesIO(real_data_buffer)

    # Converting file-like objects into dataframe
    synthetic_data = pd.read_csv(filepath_or_buffer=synthetic_data_b)
    real_data = pd.read_csv(filepath_or_buffer=real_data_b)
    
    recap = ModelService().evaluate(column_name=column_name, synthetic_data=synthetic_data, real_data=real_data)

    return Response(
        content=recap,
        media_type="application/pdf",
        headers={'Content-Disposition': 'attachment; filename="recap.pdf"'}
    )