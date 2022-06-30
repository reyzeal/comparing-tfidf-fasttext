from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO

import database
from main import eprint_retrieve
from method.fasttext.module import similarity
from tfidf.module import Testing, Generate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000","https://www.piesocket.com"])

@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify({
        'ok': True,
        'message': "Success",
        'data': database.retrieve()[:10]
    })

@app.route("/tfidf", methods=["POST"])
def tfidf_generate():
    titles = [" ".join(i['preprocessed']['result']) for i in database.retrieve()]
    Generate(titles)
    return "OK"

@app.route("/tfidf")
def tfidf():
    socketio.emit("pencarian", "Memulai pencarian")
    keyword = request.args.get("keyword")
    page = request.args.get("page") or 1
    limit = request.args.get("limit") or 10
    if type(page) is str:
        page = int(page)
    if type(limit) is str:
        limit = int(limit)
    # titles = [" ".join(i['preprocessed']['result']) for i in database.retrieve()]
    # Generate(titles)
    # Testing("game swasta")
    socketio.emit("pencarian", "Menyiapkan parameter")
    return jsonify(Testing(keyword, page, limit, socketio))

@app.route("/fasttext")
def fasttext():
    socketio.emit("pencarian", "Memulai pencarian")
    keyword = request.args.get("keyword")
    page = request.args.get("page") or 1
    limit = request.args.get("limit") or 10
    if type(page) is str:
        page = int(page)
    if type(limit) is str:
        limit = int(limit)
    socketio.emit("pencarian", "menyiapkan parameter")
    return jsonify(similarity(keyword, "model.100w3.bin", page, limit, socketio))


@app.route("/eprint-retrieve")
def eprintRetrieve():
    eprint_retrieve()
    return "ok"

@socketio.on("test")
def handle_test(data):
    print('received data:',data)
    socketio.emit("ok", data+" telah diterima")

if __name__ == "__main__":
    socketio.run(app, port=5050, debug=True)
    # app.run(port=5050, debug=True)
