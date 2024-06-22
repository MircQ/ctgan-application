import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Configuration import CONFIG
from resources import TrainingResource, GenerationResource, EvaluationResource
from services.ModelService import ModelService

if __name__ == "__main__":

    # Instantiate ModelService (singleton)
    ModelService()

    app = FastAPI(
        title="CTGAN application",
        docs_url="/apidocs"
    )

    app.include_router(router=TrainingResource.training_router)
    app.include_router(router=GenerationResource.generation_router)
    app.include_router(router=EvaluationResource.evaluation_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #uvicorn.run(app=app, host='0.0.0.0', port=4557)
    uvicorn.run(app=app, host='localhost', port=CONFIG.PORT)
