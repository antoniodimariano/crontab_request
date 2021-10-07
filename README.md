# Periodically Request for Websites metrics

#### Author Antonio Di Mariano - antonio.dimariano@gmail.com

## Description

This services runs a crontab task that periodically sends a POST request to the remote service specified in the ENV
variable
`websites_checker_service_url`
The end goal is to trigger the actions of fetching and collecting metrics for the websites specified in
the `configuration/service_configuration.json`
The default frequency of the outbound request is 2 minutes, but it can be changed by setting the ENV
variable `request_frequency`.

## Overview of the Websites Monitoring Application

The application is made of three services that can run in different systems.

There are main two services. 

The first one https://github.com/antoniodimariano/websites_metrics_collector is responsible for fetching and collecting the information from a list of URLs. The information collected is

HTTP Status returned HTTP response time regexp pattern that is expected to be found on the HTML content.
For each record, a message is produced to an Apache Kafka Topic. This service exposes a REST API Service with a POST method to accept a list of URLs to fetch and process.

The second service is https://github.com/antoniodimariano/metrics_consumer that is responsible for consuming messages about metrics being produced to an Apache Kafka Avro Topic by a different service. The main action of this service is to store the incoming message into a PostgreSQL database.

The last one is a Celery Beat based service https://github.com/antoniodimariano/crontab_request that periodically send a POST request with a list of URLS to the `websites_metrics_collector`

So, to run all the whole application,  you don't need to clone the three repos,  You can use these two public python packages

1. https://pypi.org/project/websites-metrics-consumer/ 
2. https://pypi.org/project/websites-metrics-collector/

Create two `python` applications. One will consume messages 

`pip3 install websites-metrics-consumer`

The other will produce metrics 

`pip3 install websites-metrics-collector`

In order to produce metrics, the https://github.com/antoniodimariano/websites_metrics_collector runs a REST Server with a `POST` `/api/v1/websites_metrics` endpoint that accepts a list of URLs to fetch. 
For the complete documentation go here https://github.com/antoniodimariano/websites_metrics_collector/blob/master/README.md

The last application (https://github.com/antoniodimariano/crontab_request) uses Celery Beat to periodically run the task of reading a list or URLs from a local `json` file and will send it to as payload.
of the `POST` request to `/api/v1/websites_metrics`
It requires `Redis` as broker.

You can decide not to use https://github.com/antoniodimariano/crontab_request and implements your own way of requesting a list or URLs to monitor. 
As long as you send a POST Request to the endpoint `/api/v1/websites_metrics` metrics will be collected, messages will be produced and data will be stored. 
I decided to use Celery and not, for instance, a simple timer implemented with Thread or 3-party libs because Celery is robust, scalable and production ready.
I know it comes at the price of having a broker, but I prefer to pay a small price for a significant advance. Not to mention, I am a big fan of Celery!


# How to Run this service


# Requirements

* Python >=3.8
* Redis 

# Dependencies

* requests==2.26.0
* celery==4.4.0
* redis==3.3.11

# Run

* Start Celery Beat

`beat -A crontab_tasks -l info`

* Start Celery CronTab

`worker --purge -A crontab_tasks -l info -Q request_websites_metrics -c 1 -O fair -n request_websites_metrics`

# Service ENV configuration

| ENV Variable  | VALUE | DESCRIPTION                                                                       |
|---------------|------|------------------------------------------------------------------------------------|
| celery_broker_url   | string    | Required. The FQDN or the Redis server to be used as broker |
| websites_checker_service_url    | string   | Required. The FQDN of the `websites_metrics_collector` service where to send the requests.|
| request_frequency    | string   | Optional. The default value is `*/2` 2 minutes. It express the frequency of the task. See here https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html#crontab-schedules|
| logging_level    | string   | Optional. The level of logging to use fo the built-in `logging` package. The default is `logging.INFO`|
