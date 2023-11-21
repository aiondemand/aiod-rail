FROM python:3.9
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install torch==2.0.0+cpu --index-url https://download.pytorch.org/whl/cpu
