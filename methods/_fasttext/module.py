from preprocessing import preprocessing


def similarity(modelname):
    from gensim.models import FastText
    model = FastText.load_fasttext_format(modelname)
    q, _ = preprocessing(query)
    with open("%s.bin" % docset_name, 'rb') as f:
        docset = pickle.load(f)
    result = []
    for [_id, preprocessed] in docset:
        result.append((_id, model.wv.n_similarity(q, preprocessed)))
    result = sorted(result, key=lambda x: x[1], reverse=True)
    return result