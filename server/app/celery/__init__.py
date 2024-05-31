from celery import Celery


celery = Celery(__name__, broker='amqp://guest:guest@rabbitmq:5672//')
