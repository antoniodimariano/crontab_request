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
