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
    return jsonify([])

@app.route("/transform", methods=["POST"])
def transform():
    # if dict
    #     for k, v in ...
    #         transform(v, **data)
    # if list
    #     for v in ...
    #         transform(v, **data)
    # else
    #     transform(v, **data)

    try:
        data = json.loads(request.data)
    except:
        abort(400)

    if not data:
        abort(400)

    transform = registry.lookup(data['transform'])
    if not transform:
        abort(400)

    output = transform.transform(data['inputs'])

    return jsonify(output=output)

if __name__ == "__main__":
    app.run(debug=True)
