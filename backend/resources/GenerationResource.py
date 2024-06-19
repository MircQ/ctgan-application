from fastapi import APIRouter

router = APIRouter(
    tags=["Generation"]
)


@router.post(
    path="/generate",
    summary="",
    description=""
)
def generate(samples: int):
    pass
