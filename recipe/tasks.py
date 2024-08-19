from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from recipe.models import Recipe
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
import logging
import time

logger = logging.getLogger('recipe')

@shared_task
def add(x, y):
    time.sleep(2)  
    return x + y


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def long_running_task(self):
    try:
        time.sleep(30)
        return "Task completed successfully"
    except SoftTimeLimitExceeded:
        raise self.retry(countdown=60)
    except Exception as e:
        raise self.retry(exc=e)


@shared_task
def send_email(subject, message, recipient_list):
    logger.info('Sending email: subject=%s, recipients=%s', subject, recipient_list)

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Ensure this is configured in your settings
        recipient_list,
        fail_silently=False,
    )

@shared_task
def send_daily_notifications():
    try:
        recipes = Recipe.objects.all()        
        for recipe in recipes:
            logger.info(f"author mail {recipe.author}")
            like_count = recipe.get_total_number_of_likes()
            if like_count > 0:
                logger.info(f"Recipe '{recipe.title}' has {like_count} likes")
                
                return send_mail(
                    'Daily Recipe Notification',
                    f"Your recipe '{recipe.title}' has {like_count} likes today!",
                    settings.DEFAULT_FROM_EMAIL,
                    [recipe.author],  # Assuming the recipe author has an email field
                    fail_silently=False,
                )
                
    except Exception as e:
        logger.error(f"Error sending daily notifications: {e}")
