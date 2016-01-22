import os
import json
import registry

from flask import Flask, jsonify, request, abort, render_template
app = Flask(__name__)

registry.make_registry()


"""
GET / -> list of transforms
GET /fields -> fields for this transform
POST /transform -> run the transform
"""

@app.route("/")
def hello():
    data = request.args
    transforms = registry.getall(category=data.get('category'))
    return jsonify(transforms=[v.to_dict() for v in transforms])


@app.route("/fields")
def fields():
    data = request.args
    if not data:
        abort(400)

    transform = registry.lookup(data.get('transform'), category=data.get('category'))
    if not transform:
        abort(400)

    inputs = data.get('inputs')
    fields = transform._fields_internal(inputs=inputs)

    return jsonify(fields=fields)


@app.route("/transform", methods=["POST"])
def transform():
    try:
        data = json.loads(request.data)
    except:
        abort(400)

    if not data:
        abort(400)

    transform = registry.lookup(data.get('transform'), category=data.get('category'))
    if not transform:
        abort(400)

    inputs = data.get('inputs')

    outputs = transform_many(transform, inputs, data)

    return jsonify(outputs=outputs)


@app.route('/tester', methods=['GET', 'POST'])
def tester():
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

    return render_template('tester.html', transforms=registry.getall(), inputs=smart_dump(inputs), outputs=smart_dump(outputs))


def smart_dump(v):
    """
    if the value is a string, just return it because that's ok to display...
    otherwise, json dumps it!

    """
    if isinstance(v, basestring) or isinstance(v, str):
        return v
    else:
        return json.dumps(v)


def transform_many(transform, inputs, data):
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
