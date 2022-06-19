from flask import Flask, jsonify
from flask_cors import CORS

import database
from main import eprint_retrieve

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify({
        'ok': True,
        'message': "Success",
        'data': database.retrieve()[:10]
    })


@app.route("/eprint-retrieve")
def eprintRetrieve():
    eprint_retrieve()
    return "ok"


if __name__ == "__main__":
    app.run(port=5050, debug=True)
