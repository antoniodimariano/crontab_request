from crontab_tasks.celery import app
import os
from messaging_middleware.utils.logger import Logger
from communication.RESTclient import RestClient
logger = Logger(ssl=os.environ.get('security_protocol', 0))

@app.task(queue='labs-availability-checker')
def periodically_request_available_labs_report():

    rest_client = RestClient()
    service_url = os.environ.get('tc_new_labs_deployment_trigger_rest_client')

    ret = rest_client.make_REST_request(service_url=service_url,method='GET')
    if ret:

        logger.logmsg('info', 'CRONTAB TASK COMPLETED')
    else:
        logger.logmsg('info', 'ERROR communicating with ',service_url)