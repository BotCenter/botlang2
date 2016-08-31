import requests


def build_response_dict(request_response):

    response_dict = {
        'response-object': request_response,
        'status-code': request_response.status_code,
        'headers': request_response.headers,
        'encoding': request_response.encoding,
        'content': request_response.content
    }
    try:
        response_dict['json'] = request_response.json()
    except ValueError:
        pass

    return response_dict


def http_get(url):

    response = requests.get(url)
    return build_response_dict(response)


def http_post(url, data):

    response = requests.post(url, data)
    return build_response_dict(response)
