import os
from celery.schedules import crontab

broker_url = os.environ.get('CELERY_BROKER_URL')
result_backend = os.environ.get('CELERY_RESULT_BACKEND')

# task_serializer = 'json'
# result_serializer = 'json'
# accept_content = ['json']
# timezone = 'US/Pacific'
# enable_utc = True

beat_schedule = {
    'download-closing-prices-eod': {
        'task': 'LotDividerAPI.tasks.getClosingData',
        'schedule': crontab(hour=4, minute=0, day_of_week=[2,3,4,5,6]), # UTC Time
    },
    # 'download-closing-prices-test': {
    #     'task': 'LotDividerAPI.tasks.getClosingData',
    #     'schedule': crontab(hour=21, minute=15, day_of_week=[3]),
    # },
}