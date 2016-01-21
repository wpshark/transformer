from flask import Flask, jsonify
app = Flask(__name__)

from registry import make_registry, getall
make_registry()


"""
GET / -> list of transforms
GET /fields -> fields for this transform
POST /transform -> run the transform
"""

@app.route("/")
def hello():
    return jsonify(transforms=getall())

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

    return jsonify("hello world")

if __name__ == "__main__":
    app.run(debug=True)
