FROM python:3.10

WORKDIR /code

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY migrate_aiod_ids.py ./

CMD ["/bin/sh", "-c", "python migrate_aiod_ids.py"]
