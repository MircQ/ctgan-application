import io
from typing import Literal

import pandas as pd
from fastapi import APIRouter, UploadFile

from services.ModelService import ModelService

training_router = APIRouter(
    tags=["Training"]
)


@training_router.post(
    path="/train/{model}",
    summary="Train a model",
    description="Train the given model using the data passed as parameter"
)
async def train(model: Literal["CTGAN", "TVAE"], file: UploadFile) -> str:

    # Reading file as bytes
    buffer = await file.read()

    # Convert into file-like object
    data = io.BytesIO(buffer)

    # Converting file into dataframe
    df = pd.read_csv(filepath_or_buffer=data)

    # Model training
    ModelService().train(model=model, data=df)

    return "Model correctly trained"

