from messaging_middleware.utils.logger import Logger
from helpers.endpoints_error_response import build_error_response
from helpers.operation_with_files import read_service_configuration
import json
import os
from aiohttp import web
from celery_tasks import tasks

bad_payload = "Bad format!No squealing, remember that it's all in your head"
msg_503 = "The server is currently unable to handle the request due to a temporary overloading or missing microservices' dependency "
logger = Logger(ssl=os.environ.get('security_protocol', 0))


def json_error(message, status=404):
    return web.Response(
        body=json.dumps({'error': message}).encode('utf-8'),
        content_type='application/json', status=status)


endpoint_to_validate = [
    {
        'url': '/api/lab/provisioning/check_availability',
        'query_params': '',
        'headers': '',
        'method': 'GET',
        'function': 'check_availability'
    }

]


@web.middleware
async def endpoints_validation(request, handler):
    """

    :param request:
    :param handler:
    :return:
    """

    for endpoint in endpoint_to_validate:
        url_has_variable_resource = ':' in endpoint['url']

        if request.path == endpoint['url'] and request.method == endpoint['method']:

            return await process_endpoint(endpoint, handler, request)
        elif url_has_variable_resource:
            original_path = request.path
            endpoint_tail = endpoint['url']
            try:
                original_path = str(request.path).split('/')[len(endpoint['url'].split('/')) - 1]
                endpoint_tail = endpoint['url'].split('/')[len(endpoint['url'].split('/')) - 1]
            except Exception as missing_value:
                pass
            if original_path == endpoint_tail:
                return await process_endpoint(endpoint, handler, request)

    logger.logmsg('error', 'Middleware endpoints_validation finished with error', request.path)
    return json_error({}, 404)


async def process_endpoint(endpoint, handler, request):
    for params in endpoint['query_params']:
        logger.logmsg('debug', "Query parms:", params, endpoint['url'])
        if (request.query.get(params, None)) is None:
            logger.logmsg('error', 'Missing query param(s):', params)
            return json_error(bad_payload, 400)
        if (request.query.get(params, None)) == '':
            logger.logmsg('error', 'empty query param(s):', params)
            return json_error(bad_payload, 400)
    for header in endpoint['headers']:
        if (request.headers.get(header, None)) is None:
            logger.logmsg('error', 'Missing header(s):', header)
            return json_error(bad_payload, 401)
    if 'body' in endpoint and request.method == 'POST' or request.method == 'PUT':
        try:
            body = await request.json()
            for field in endpoint['body']:
                if (body.get(field, None)) is None:
                    logger.logmsg('error', 'Missing payload field(s):', field)
                    return json_error(bad_payload, 400)
                # if (body.get(field, None)) == '':
                #     logger.logmsg('error', 'empty body param(s):', field)
                #     return json_error(bad_payload, 400)

        except ValueError as e:
            logger.logmsg('error', "ERROR BODY IS EMPTY")
            return json_error(bad_payload, 400)
    request['endpoint'] = endpoint
    response = await handler(request)

    logger.logmsg('debug', 'Middleware endpoints_validation finished:', request['endpoint'])
    return response


class Handler:

    def __init__(self, **kwargs):
        self.logger = logger

    async def endpoints_dispatcher(self, request):
        """
        Dispatches endpoints' functions

        :param request:
        :return:
        """
        self.logger.logmsg('info', "[endpoints_dispatcher PATH:]:", request.path, request.method)
        method_name = request.get('endpoint', dict()).get('function', '')
        method = None
        try:
            method = getattr(self, method_name)
        except AttributeError:
            self.logger.logmsg('error', "FATAL,wrong endpoints definition!")
            return web.json_response({}, status=503, content_type='application/json', dumps=json.dumps)

        result = await method(request)
        if isinstance(result, dict):
            if request.method == 'POST' or request.method == 'PUT':
                status_code = result.get('status_code', 201)
            else:
                status_code = result.get('status_code', 200)
            result.pop('status_code', None)
        elif isinstance(result, list):
            if request.method == 'POST' or request.method == 'PUT':
                status_code = 201
            else:
                status_code = 200
        else:
            status_code = 403
            if result != 0:
                status_code = result
            result = build_error_response(error_status=status_code)
        return web.json_response(result, status=status_code, content_type='application/json', dumps=json.dumps)

    async def check_availability(self, request):
        """

        :param request:
        :return:
        """
        try:

            data = request
            data_header = request.headers

            configuration_path = os.path.abspath('configuration/service_configuration.json')
            external_rest_services = read_service_configuration(
                configuration_file=configuration_path, section='external_rest_services')

            persistence_conf = read_service_configuration(configuration_file=configuration_path,
                                                          section='persistence_conf')

            tasks.check_available_labs_and_store_for_each_template_and_dc.apply_async(

                kwargs={"external_rest_services": external_rest_services,
                        "persistence_conf": persistence_conf
                        },
                retry=True,
                countdown=3,
                retry_policy={
                    'max_retries': 3,
                    'interval_start': 0,
                    'interval_step': 0.2,
                    'interval_max': 0.2,
                }

            )

            return {}
        except Exception as error:
            return 0

    def start_server(self):
        self.logger.logmsg('info', "STARTING THE REST SERVER....")
        app = web.Application(middlewares=[endpoints_validation])
        app.router.add_get('/api/lab/provisioning/check_availability', self.endpoints_dispatcher)

        web.run_app(app, host=os.environ.get('SERVICE_HOST', 'localhost'),
                    port=int(os.environ.get('SERVICE_LISTEN_PORT', '6200')))
