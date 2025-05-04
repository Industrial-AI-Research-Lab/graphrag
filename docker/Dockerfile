FROM python:3.12.9-bullseye

WORKDIR /src

RUN apt-get update && apt-get install -y \
    nano wget curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY dist/graphrag-2.1.0-py3-none-any.whl .

RUN pip install graphrag-2.1.0-py3-none-any.whl

CMD ["graphrag"]

