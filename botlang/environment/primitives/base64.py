import base64


def base64_encode(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')


def base64_decode(text):
    return base64.b64decode(text.encode('utf-8')).decode('utf-8')


EXPORT_FUNCTIONS = {
    'b64-encode': base64_encode,
    'b64-decode': base64_decode
}
