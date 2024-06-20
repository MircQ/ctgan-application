from typing import Literal

from fastapi import APIRouter

from services.ModelService import ModelService

router = APIRouter(
    tags=["Training"]
)


@router.post(
    path="/train/{model}",
    summary="Train a model",
    description="Train the given model using the data passed as parameter"
)
def train(model: Literal["CTGAN", "TVAE"], data):

    ModelService().train(model=model, data=data)

