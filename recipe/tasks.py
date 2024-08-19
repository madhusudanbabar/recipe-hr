from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

import time

@shared_task
def add(x, y):
    time.sleep(10)  
    return x + y


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def long_running_task(self):
    try:
        time.sleep(30)
        return "Task completed successfully"
    except SoftTimeLimitExceeded:
        # Handle soft time limit exceeded
        raise self.retry(countdown=60)
    except Exception as e:
        # Handle other exceptions
        raise self.retry(exc=e)
