import time
import psycopg2
from django.conf import settings

def wait_for_db(max_retries=5, delay_seconds=5):
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                dbname=settings.DATABASES['default']['NAME'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                host=settings.DATABASES['default']['HOST'],
                port=settings.DATABASES['default']['PORT'],
                connect_timeout=3
            )
            conn.close()
            return True
        except psycopg2.OperationalError as e:
            if i == max_retries - 1:
                raise
            time.sleep(delay_seconds)
    return False