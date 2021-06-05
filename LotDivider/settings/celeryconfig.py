from celery.schedules import crontab

broker_url = 'redis://127.0.0.1:6379/0'
result_backend = 'redis://127.0.0.1:6379/0'

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
    #     'schedule': crontab(hour=4, minute=56, day_of_week=[6]),
    # },
}