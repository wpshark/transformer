
import os
import sys
import json

from logging.config import dictConfig

import requests

from deepdiff import DeepDiff

# insert the root dir into the system path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from transformer import registry
from transformer.util import APIError

from flask import Flask, jsonify, request


# Create our Flask App
app = Flask(__name__)

dictConfig({
    'version': 1,
    'formatters': {'default': {}},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

sentry_dsn = os.environ.get('SENTRY_DSN')
if sentry_dsn:
    from raven.contrib.flask import Sentry
    sentry = Sentry(app, dsn=sentry_dsn)


# Prepare the application transform registry
registry.make_registry()

live_integration_test_server = os.environ.get('LIVE_INTEGRATION_TEST_SERVER')
live_integration_test_timeout = os.environ.get('LIVE_INTEGRATION_TEST_TIMEOUT', 10)


@app.after_request
def perform_live_integration_test(response):
    if live_integration_test_server:
        try:
            test_response = requests.request(
                method=request.method,
                url=live_integration_test_server + request.path,
                params=request.args,
                data=request.data,
                timeout=live_integration_test_timeout
            )

            if response.status_code == test_response.status_code:
                app.logger.debug('[perform_live_integration_test] Status codes match!')
            else:
                app.logger.error(
                    '[perform_live_integration_test] Status codes do not match: %s != %s',
                    response.status_code,
                    test_response.status_code
                )

            body_diff = DeepDiff(response.json, test_response.json(), ignore_order=True)
            if not body_diff:
                app.logger.debug('[perform_live_integration_test] Bodies match!')
            else:
                app.logger.error('[perform_live_integration_test] Bodies do not match: %s', body_diff)
        except Exception as e:
            app.logger.error('[perform_live_integration_test] Exception trying to run live integration test: %s', e)
    return response


@app.route('/')
def hello():
    """ Returns a list of transforms available to be used """
    data = request.args
    transforms = registry.get_all(category=data.get('category'))
    return jsonify(transforms=[v.to_dict() for v in transforms])


@app.route('/fields')
def fields():
    """ Returns a list of fields for a given transform """
    data = request.args
    if not data or 'transform' not in data:
        return jsonify(fields=[])

    transform = registry.lookup(data['transform'], category=data.get('category'))
    if not transform:
        raise APIError('Transform "{}" not found'.format(data['transform']), 404)

    inputs = data.get('inputs')
    fields = transform.all_fields(inputs=inputs)

    return jsonify(fields=fields)


@app.route('/transform', methods=["POST"])
def transform():
    """ Perform a transformation """
    try:
        data = json.loads(request.data)
    except:
        raise APIError('Missing or malformed request body', 400)

    if not data:
        raise APIError('Missing request body', 400)

    if 'inputs' not in data:
        data['inputs'] = ''

    # Each of these gets popped off so that we don't pass it along in the
    # options to the transform function
    inputs = data.pop('inputs')
    transform_name = data.pop('transform', '')
    category = data.pop('category', '')

    if not transform_name:
        raise APIError('Missing transform', 400)

    transform = registry.lookup(transform_name, category=category)
    if not transform:
        raise APIError('Transform "{}" not found'.format(transform_name), 404)

    outputs = transform.transform_many(inputs, data)

    return jsonify(outputs=outputs)


@app.errorhandler(APIError)
def error(e):
    """ Handle our APIError exceptions """
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response


@app.errorhandler(Exception)
def exception(e):
    """ Handle generic exceptions """
    response = jsonify(message=str(e))
    response.status_code = 500
    return response


def serve_locally(app):
    """
    serve this flask application locally

    """
    port = int(os.environ.get('PORT', 5000))
    debug = True if os.environ.get('DEBUG', 'false') == 'true' else False
    host = os.environ.get('HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    serve_locally(app)
