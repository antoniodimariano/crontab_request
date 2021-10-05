from crontab_tasks.celery import app
import os
import logging
import requests
from helpers.operation_with_files import read_service_configuration

logger = logging.getLogger()
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO
)
logger.setLevel(logging.INFO)
@app.task(queue='request_websites_metrics')
def periodically_request_websites_metrics() -> int:
    """
    This function loads the list of URLs from the configuration/service_configuration.json
    and use it as payload for the POST request that will be sent to websites_checker_service_url
    :return:
    """
    # Making a get request
    configuration_path = os.path.abspath('configuration/service_configuration.json')
    list_of_websites_to_check = read_service_configuration(
        configuration_file=configuration_path, section='list_of_websites_to_check')
    try:

        remote_service_url = os.environ.get('websites_checker_service_url','http://192.168.1.101:8080/api/v1/websites_metrics')
        response = requests.post(url=remote_service_url, json=list_of_websites_to_check)
        if response:
            logger.info(f"The request has been sent to {remote_service_url} with payload: {list_of_websites_to_check}")

        else:
            logger.error(f"Error contacting the service {remote_service_url}")
    except Exception as error:
        logger.error(f"The Exception {error} occurred")
    return 1
