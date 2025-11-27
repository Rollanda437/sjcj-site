# api/index.py – Handler Vercel pour Django
from wsgiref.simple_server import make_server
from django.core.wsgi import get_wsgi_application
import os

application = get_wsgi_application()

def handler(request):
    # Vercel appelle cette fonction pour chaque requête
    environ = {
        'wsgi.input': request['body'],
        'CONTENT_LENGTH': str(len(request['body'])),
        'CONTENT_TYPE': request['headers'].get('content-type', ''),
        'REQUEST_METHOD': request['method'],
        'PATH_INFO': request['path'],
        'QUERY_STRING': request['query'],
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'SERVER_NAME': request['headers'].get('host', 'localhost'),
        'SERVER_PORT': '80',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': request['headers'].get('x-forwarded-proto', 'http'),
        'wsgi.errors': os.sys.stderr,
    }

    for key, value in request['headers'].items():
        if key.startswith('http-'):
            environ[f'HTTP_{key.upper().replace("-", "_")}'] = value

    status = [None]
    response_headers = [None]
    response_body = []

    def start_response(status_code, headers):
        status[0] = status_code
        response_headers[0] = headers

    def write(chunk):
        response_body.append(chunk)

    application(environ, start_response, write)

    return {
        'statusCode': int(status[0].split()[0]),
        'headers': dict(response_headers[0]),
        'body': b''.join(response_body)
    }