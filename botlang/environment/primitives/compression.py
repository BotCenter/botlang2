import base64
import bz2


def bz2_compress(string):

    return base64.b64encode(
        bz2.compress(string.encode('utf-8'))
    ).decode('ascii')


def bz2_decompress(b64_string):

    return bz2.decompress(
        base64.b64decode(b64_string.encode('ascii'))
    ).decode('utf-8')


EXPORT_FUNCTIONS = {
    'bz2-compress': bz2_compress,
    'bz2-decompress': bz2_decompress
}
