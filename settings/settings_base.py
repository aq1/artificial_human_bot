import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOGS_PATH = os.path.join(BASE_DIR, 'logs')


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = ''
MONGO_USER = ''
MONGO_PASSWORD = ''

FREELANCER_TOKEN = ''

TELEGRAM_TOKEN = ''

ADMINS = []

POLONIEX_KEY = ''
POLONIEX_SECRET = ''

CELERY_PROJECT_NAME = ''
CELERY_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_BROKER = 'redis://127.0.0.1:6379/0'

PID_PATH = '/var/run/artificial_human_bot.pid'
