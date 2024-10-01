import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.ping_render, 'interval', minutes=10)
        scheduler.start()

    @staticmethod
    def ping_render():
        url = 'https://onesmus-kimanzi.onrender.com'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print('Successfully pinged Render instance')
            else:
                print(f'Failed to ping Render instance, status code: {response.status_code}')
        except requests.ConnectionError:
            print('Error connecting to Render instance')
