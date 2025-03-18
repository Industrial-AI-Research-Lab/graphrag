FROM python:3.12.9-bullseye

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY dict/graphrag-2.1.0-py3-none-any.whl .

RUN pip install graphrag-2.1.0-py3-none-any.whl

CMD ["graphrag"]

