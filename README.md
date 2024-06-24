# ctgan-application

*ctgan-application* is a simple application that permits to interact with CT-GAN and T-VAE models.

## Architecture overview

![image](https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fdrive.google.com/uc?id=1oSbnhvuOQBIwBWRziQQ10rtmzx2nkPZj)

## Technologies

### Backend
[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![pytorch](https://img.shields.io/badge/PyTorch-2.3.1-EE4C2C.svg?style=flat&logo=pytorch)](https://pytorch.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)

### Frontend
[![node](https://img.shields.io/badge/Node.js-20.15.0-43853D.svg?style=flat&logo=node.js&logoColor=white)](https://nodejs.org/en)
[![node](https://img.shields.io/badge/Angular-18.0.5-DD0031.svg?style=flat&logo=angular&logoColor=white)](https://angular.dev/)

## Launching the application

You can launch *ctgan-application* in two ways, using Docker to containerize the application or by simply launching
backend and frontend separately.

### Docker

If you have Docker installed on your machine, simply run the following command from the root path of the project:
```shell
docker compose up
```

This command will create both the docker images for frontend and backend, and run them automatically. Since the
generated images are quite big (backend is about 5GB), this process can take a few minutes. 



### Standalone
If you don't have Docker installed on your machine, make sure to have the correct versions of Python (3.11), Node.js 
(20.0.15) and Angular (18.0.5) installed. 

In order to start the backend, move into the backend project and create a virtual environment using the following 
command:

```shell
python -m venv venv
```

To activate the virtual environment, run the following command on Windows:

```shell
venv\Scripts\activate
```

Otherwise, launch the following command if you are on Linux:

```shell
source venv/bin/activate
```

Finally, start the backend using the following command:

```shell
python main.py
```

In order to start the frontend, move into the *frontend* project and launch the following command:

```shell
ng serve
```

## User Guide
Services will be exposed as follows:

- frontend will be exposed at http://localhost:4200
- backend will be exposed at http://localhost:4201

In order to use the application, simply connect to http://localhost:4200.

In order to use the Swagger, simply connect to http://localhost:4201/apidocs.

In case you are using the UI, the start and the end of the training of a model will be notified by a snackbar notification. In
order to reduce the waiting time, the number of epochs for which a model is trained has been reduced.

In case you are using the Swagger, you can directly upload the files from the Swagger interface as well as download the
results.

*ctgan-backend* exposes three APIs:

- */train*,  which trains a model using the given data
- */generate*, which generate synthetic data using the previously trained model and download the generated data into a .csv file
- */evaluate*, which generates an evaluation report given a column and downloads the report in .pdf format


## Known Issues and Limitations
This project is intended to be a concept and because of that it is not production-ready. Here is a list of
know issues, limitations and possible improvements:

- validation on stepper component is missing.
- number of epochs for which the model is trained has been reduced in order to improve the user experience.
- environment variables management on client side is missing, meaning that always the same ports will be exposed.
- communication between containers can be improved. At the moment, containers use the port exposed on the hosting machine to communicate because of CORS policy reasons (ideally, they can communicate directly using the Docker network).
- CSS part has been voluntarily neglected
- *ctgan-backend*'s performances have not been improved by using Python compilers such as Nuitka
- synthetic data generation is performed using the last trained model
