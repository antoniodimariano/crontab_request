import json
from typing import Optional


def read_service_configuration(configuration_file: str, section: Optional[int] = 0) -> dict:
    """
    This function loads the JSON content from the given configuration_file
    if section is specified, the function will return the content of the key section

    :param configuration_file:
    :param section:
    :return:
    """
    try:

        if section:
            service_configuration = json.load(open(configuration_file)).get(section)
        else:
            service_configuration = json.load(open(configuration_file))
        return service_configuration
    except Exception as error:
        print("EXCEPTION opening service configuration:", error)
        return 0
