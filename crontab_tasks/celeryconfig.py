import os
broker_url = os.environ.get('celery_broker_url')
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Rome'
redis_password = os.environ.get('celery_broker_pwd')
enable_utc = True
