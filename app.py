import json
import registry

from flask import Flask, jsonify, request, abort
app = Flask(__name__)

registry.make_registry()


"""
GET / -> list of transforms
GET /fields -> fields for this transform
POST /transform -> run the transform
"""

@app.route("/")
def hello():
    return jsonify(transforms=registry.getall())

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

    return jsonify(outputs=outputs)

if __name__ == "__main__":
    app.run(debug=True)
