
# New Labs Deployment Trigger

# Description 

This services runs a crontab task that periodically sends a GET request to the service http://tc-new-labs-deployment-trigger-rest-server:3000/api/lab/provisioning/check_availability.
The end goal is to trigger the actions of checking if new resources are needed.
The default frequency of the outbound request is 2 mins but it can be changed by setting the ENV variable `request_frequency`. 


# Requirements

* Python >=3.6

# Dependencies

* requests
* celery==4.4.0
* redis==3.3.11
* microservices_messaging_layer==1.0.22
* configuration-layer==1.0.17
* aiohttp==3.6.2

# Run

* First start Celery 

`worker --purge -A celery_taks -A crontab_tasks -l info -Q available-resources-announcer -c 1 -O fair -n available-resources-announcer`

* Secondly start the REST server with 

`python main`


# Run test 

`python -m unittest test/test_available_labs.py`



# Environment variable for Testing 

same as staging


# Environment variable for Celery  on Production

| ENV Variable  | VALUE | DESCRIPTION                                                                       |
|---------------|------|------------------------------------------------------------------------------------|
| celery_broker_url   | string    | Required. The FQDN or the Redis server to be used as broker |
| brokers    | string   | Required. The FQDN of the Confluent Kafka Brokers.|
| schema_registry               | string   | Required. The FQDN of the Confluent Kafka Service Registry.|
| service_name                    |tc-new-labs-deployment-trigger   | Required. The service name.|



# Environment variable for Celery on Staging


| ENV Variable  | VALUE | DESCRIPTION                                                                       |
|---------------|------|------------------------------------------------------------------------------------|
| celery_broker_url   | string    | Required. The FQDN or the Redis server to be used as broker |
| brokers    | string   | Required. The FQDN of the Confluent Kafka Brokers.|
| schema_registry               | string   | Required. The FQDN of the Confluent Kafka Service Registry.|
| service_name                     |tc-new-labs-deployment-trigger  | Required. The service name.|