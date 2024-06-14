FROM python:3.8

RUN pip install --upgrade pip

WORKDIR /lab2

COPY requirements.txt /lab2
RUN pip install -r requirements.txt

COPY main.py /lab2

CMD ["python", "main.py"]
