FROM python:3.11-slim as base

WORKDIR /app

COPY . .

# Forcing installing torch version without GPU support
RUN python -m pip install torch==2.3.1 --index-url https://download.pytorch.org/whl/cpu

# Installing project requirements
RUN python -m pip install -r requirements.txt

CMD ["python", "main.py"]