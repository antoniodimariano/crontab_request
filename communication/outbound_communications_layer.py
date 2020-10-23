# Created by Antonio Di Mariano (antonio_dimariano@trendmicro.com) at 2019-07-03
from messaging_middleware.confluent_producer.AVROProducer import AVROPRODUCER
import os
import datetime
from datetime import datetime, timezone

default_key_value = {"service_name": os.environ.get('service_name')}


class OutboundCommunicationLayer:

    def __init__(self, **kwargs):
        self.producer = AVROPRODUCER(
            brokers_uri=kwargs.get('brokers_uri'),
            schema_registry_url=kwargs.get('schema_registry_url'),
            topic=kwargs.get('topic'),
            security_protocol=kwargs.get('security_protocol', 'plaintext'),
            sasl_mechanisms=kwargs.get('sasl_mechanisms'),
            sasl_username=kwargs.get('sasl_username'),
            sasl_password=kwargs.get('sasl_password'),
            basic_auth_credentials_source=kwargs.get(
                'schema_registry_basic_auth_credentials_source'),
            basic_auth_user_info=kwargs.get('schema_registry_basic_auth_user_info')
        )

    def log_message_to_kafka(self, message,fill_data=1):
        try:
            if fill_data:

                message['service_name'] = os.environ.get('service_name')
                message['cloud'] = 'vcloud'
                message['timestamp'] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

            self.producer.produce_message(value=message, key=default_key_value)
            return 1
        except Exception as error:
            print("EXCEPTION SENDING MSG TO KAFKA %s %s:" % (message, error))
            return 0
