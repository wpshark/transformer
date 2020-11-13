from __future__ import absolute_import

import collections
import os
import sys
import json

from celery import Celery
from deepdiff import DeepDiff
import requests

# insert the root dir into the system path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from transformer import registry
from transformer.util import APIError

from flask import Flask, jsonify, request


# Create our Flask App
app = Flask(__name__)

sentry_dsn = os.environ.get('SENTRY_DSN')
if sentry_dsn:
    from raven.contrib.flask import Sentry
    sentry = Sentry(app, dsn=sentry_dsn)

app.config['CELERY_BROKER_URL'] = os.environ.get('REDIS_URL')

celery = Celery('transformer.app', broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# Prepare the application transform registry
registry.make_registry()

# Configure live integration testing

live_integration_test_server = os.environ.get('LIVE_INTEGRATION_TEST_SERVER')


def str_to_unicode(data):
    if isinstance(data, basestring):
        return unicode(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(str_to_unicode, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(str_to_unicode, data))
    else:
        return data


@celery.task
def perform_async_live_integration_server_test(method, path, args, data, expected_status_code, expected_json):
    response = requests.request(method=method, url=live_integration_test_server + path, params=args, data=data)

    body_diff = DeepDiff(expected_json, response.json(), ignore_order=True)
    full_match = expected_status_code == response.status_code and not body_diff

    if full_match:
        print '[perform_live_integration_test] Responses match!'
    else:
        output = '[perform_live_integration_test] Responses do not match:\n' \
                 'path: %s\ndata: %s\nexpected status code: %s\nactual status code: %s\njson diff: %s' % \
                 (path, data, expected_status_code, response.status_code, body_diff)

        print output


@app.after_request
def perform_live_integration_test(response):
    if live_integration_test_server:
        perform_async_live_integration_server_test.delay(
            request.method, request.path, request.args, request.data, response.status_code, response.json)

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
    if not data or u'transform' not in data:
        return jsonify(fields=[])

    transform = registry.lookup(data['transform'], category=data.get(u'category'))
    if not transform:
        raise APIError('Transform "{}" not found'.format(data['transform']), 404)

    inputs = data.get(u'inputs')
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

    if u'inputs' not in data:
        data[u'inputs'] = ''

    # Each of these gets popped off so that we don't pass it along in the
    # options to the transform function
    inputs = data.pop(u'inputs')
    transform_name = data.pop(u'transform', u'')
    category = data.pop(u'category', u'')

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
