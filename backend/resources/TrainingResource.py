from typing import Literal

from fastapi import APIRouter

from services.ModelService import ModelService

router = APIRouter(
    tags=["Training"]
)


@router.post(
    path="/train",
    summary="",
    description=""
)
def train(model: Literal["CTGAN", "TVAE"], data):

    ModelService().train()

    discrete_columns = [
        'workclass',
        'education',
        'marital-status',
        'occupation',
        'relationship',
        'race',
        'sex',
        'native-country',
        'income'
    ]

    ctgan = CTGAN(epochs=10)
    ctgan.fit(real_data, discrete_columns)
