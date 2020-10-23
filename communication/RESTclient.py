import logging
import requests
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

log = logging.getLogger(__name__)
default_headers = {"Content-Type": "application/json"}


class RestClient():
    __instance = None

    def __new__(cls, *args, **kwargs):
        if RestClient.__instance is None:
            RestClient.__instance = object.__new__(cls)
            RestClient.good_status = [200, 201, 202, 203, 204, 206, 207, 208, 226]
            RestClient.redirection_status = [300, 301, 302, 303, 304, 305, 306, 307, 308]
            RestClient.client_error_status = list(range(400, 451))
            RestClient.internal_server_error = [500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511]
        return RestClient.__instance

    def requests_retry_session(self,
                               retries=3,
                               backoff_factor=0.3,
                               status_forcelist=(500, 502, 504),
                               session=None,
                               ):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def make_REST_request(self, service_url, method, headers={"Accept": "application/json"}, payload=None):
        try:
            if method == 'GET':
                ret = self.requests_retry_session().get(url=service_url, headers=headers, timeout=30)
            elif method == 'DELETE':
                ret = self.requests_retry_session().delete(url=service_url, headers=headers, timeout=30)
            elif method == 'POST':
                ret = self.requests_retry_session().post(url=service_url, headers=headers, json=payload,
                                                         timeout=os.environ.get('REST_CALL_TIMEOUT', 40))
            elif method == 'PUT':
                ret = self.requests_retry_session().put(url=service_url, headers=headers, json=payload,
                                                        timeout=os.environ.get('REST_CALL_TIMEOUT', 40))

            elif method == 'PATCH':
                ret = self.requests_retry_session().patch(url=service_url, headers=headers, json=payload,
                                                          timeout=os.environ.get('REST_CALL_TIMEOUT', 40))

            if ret.status_code in self.good_status:
                return {
                    "response": ret.json(),
                    "status_code": ret.status_code
                }
            else:
                return 0
        except Exception as error:
            return 0
