import requests


def build_response_dict(request_response):

    response_dict = {
        'status-code': request_response.status_code,
        'headers': request_response.headers,
        'encoding': request_response.encoding,
        'text': request_response.text
    }
    try:
        response_dict['json'] = request_response.json()
    except ValueError:
        pass

    return response_dict


def http_get(url, headers=None):

    response = requests.get(url, headers=headers)
    return build_response_dict(response)


def http_post(url, data, headers=None):

    response = requests.post(url, data, headers=headers)
    return build_response_dict(response)
