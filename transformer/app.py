from __future__ import absolute_import
import os
import sys
import json

# insert the root dir into the system path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from transformer import registry
from transformer.util import APIError

from flask import Flask, jsonify, request


# Create our Flask App
app = Flask(__name__)

# Prepare the application transform registry
registry.make_registry()


@app.route("/")
def hello():
    """ Returns a list of transforms available to be used """
    data = request.args
    transforms = registry.get_all(category=data.get('category'))
    return jsonify(transforms=[v.to_dict() for v in transforms])


@app.route("/fields")
def fields():
    """ Returns a list of fields for a given transform """
    data = request.args
    if not data:
        raise APIError('Missing Transform', 400)

    transform = registry.lookup(data.get('transform'), category=data.get('category'))
    if not transform:
        raise APIError('Transform Not Found', 404)

    inputs = data.get('inputs')
    fields = transform._fields_internal(inputs=inputs)

    return jsonify(fields=fields)


@app.route("/transform", methods=["POST"])
def transform():
    """ Perform a transformation """
    try:
        data = json.loads(request.data)
    except:
        raise APIError('Missing Body', 400)

    if not data:
        raise APIError('Invalid Body', 400)

    transform = registry.lookup(data.get('transform'), category=data.get('category'))
    if not transform:
        raise APIError('Transform Not Found', 404)

    inputs = data.get('inputs')

    outputs = transform_many(transform, inputs, data)

    return jsonify(outputs=outputs)


@app.errorhandler(APIError)
def error(e):
    """ Handle our APIError exceptions """
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response


def transform_many(transform, inputs, data):
    """
    take the inputs object and try to convert all of the inputs with the data provided

    """
    if isinstance(inputs, dict):
        outputs = {}
        for k, v in inputs.iteritems():
            outputs[k] = transform.transform(v, data=data)
    elif isinstance(inputs, list):
        outputs = []
        for v in inputs:
            outputs.append(transform.transform(v, data=data))
    else:
        outputs = transform.transform(inputs, data=data)
    return outputs


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
