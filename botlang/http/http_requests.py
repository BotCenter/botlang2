import requests


def http_get(url):

    response_dict = {}
    response = requests.get(url)
    response_dict['response_object'] = response
    response_dict['status_code'] = response.status_code
    response_dict['headers'] = response.headers
    response_dict['encoding'] = response.encoding
    response_dict['text'] = response.text

    try:
        response_dict['json'] = response.json()
    except:
        pass

    return response_dict
