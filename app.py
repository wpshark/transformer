import os
import json
import registry

from util import APIError, smart_dump

from flask import Flask, jsonify, request, render_template

# Create our Flask App
app = Flask(__name__)

# Prepare the application transform registry
registry.make_registry()


@app.route("/")
def hello():
    """ Returns a list of transforms available to be used """
    data = request.args
    transforms = registry.getall(category=data.get('category'))
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


@app.route('/tester', methods=['GET', 'POST'])
def tester():
    """ Render a really simple tester form for testing the transforms """
    inputs = request.form.get('inputs')
    outputs = None
    if request.method == 'POST':
        transform = registry.lookup(request.form.get('transform'))
        try:
            inputs = json.loads(inputs)
        except:
            if '[' in inputs or '{' in inputs:
                raise
        outputs = transform_many(transform, inputs, dict(request.form))

    return render_template('tester.html',
                            transforms=registry.getall(),
                            inputs=smart_dump(inputs),
                            outputs=smart_dump(outputs))


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


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug = True if os.environ.get('DEBUG', 'false') == 'true' else False
    host = os.environ.get('HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=debug)
