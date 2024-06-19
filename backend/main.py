import uvicorn
from fastapi import FastAPI

from resources import TrainingResource, GenerationResource

# TODO see https://www.milanwittpohl.com/projects/tutorials/full-stack-web-app/dockerizing-our-front-and-backend

if __name__ == "__main__":

    app = FastAPI()

    app.include_router(router=TrainingResource.router)
    app.include_router(router=GenerationResource.router)

    uvicorn.run(app=app, host='0.0.0.0', port=4557)
