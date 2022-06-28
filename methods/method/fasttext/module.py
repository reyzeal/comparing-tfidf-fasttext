import math
import pickle

from database import retrieve
from preprocessing import preprocessing


def similarity(query, modelname, page = 1, limit = 10, socketio = None):
    socketio.emit("pencarian", "Loading FastText")
    from gensim.models import FastText
    socketio.emit("pencarian", "menyiapkan model")
    model = FastText.load_fasttext_format(modelname)
    socketio.emit("pencarian", "preprocessing keyword")
    q, _ = preprocessing(query)
    result = []
    socketio.emit("pencarian", "pengambilan docset")
    docset = [i for i in retrieve() if 'preprocessed' in i]
    socketio.emit("pencarian", "perhitungan cosine similarity")
    for i in docset:

        i['confidence'] = float(model.wv.n_similarity(q, i['preprocessed']['result']))
        result.append(i)

    socketio.emit("pencarian", "perhitungan ranking")
    result = sorted(result, key=lambda x: x['confidence'], reverse=True)
    socketio.emit("pencarian", None)
    return {
        'data': result[(page-1)*limit:page*limit],
        'page': page,
        'limit': limit,
        'total': math.ceil(len(result) / limit),
        'hasPrev': page > 1,
        'hasNext': page < math.ceil(len(result) / limit),
        'next': page + 1 if page < math.ceil(len(result) / limit) else None,
        'prev': page - 1 if page > 1 else None,
    }
