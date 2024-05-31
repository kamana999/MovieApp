FROM python:3.9.19

WORKDIR /root

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY app /root/app
COPY app/app.py /root/app.py

CMD ["python", "app.py"]
