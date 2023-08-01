from flask import Flask, Response, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

@app.route("/fuck", methods=["GET"])
#@cross_origin()
def post_example():
    """GET in server"""
    return jsonify(message="POST request returned")

if __name__ == '__main__':
    app.run(host = "192.168.1.113", port=8000)