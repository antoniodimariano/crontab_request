
# New Labs Deployment Trigger

# Description 

This service is responsible for periodically checking the number of available labs and see if new labs are needed.
If new labs are needed, a REST request is sent to the `tc-vapps-supply-guard` and `tc-users-supply-guard`

The service uses a Celery crontab to request and send the report to the above services. 

The report received from the `tc-available-labs` service has the following data format 

```json
{"sps": {"edc2": 4}, "wfbss": {"edc2": 1}, "wfbs-std": {"edc2": 4}}

```
The payload of the request sent to the the `tc-vapps-supply-guard` service and `tc-users-supply-guard` has the following data format 


```json

{"dc_name": "edc2", "template_shortname": "sps"}

```


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
| service_name                    |tc-new-labs-deployment-trigger  | Required. The service name.|