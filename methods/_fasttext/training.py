import fasttext
model = fasttext.train_unsupervised('wiki-id-formatted.txt', model='skipgram')
model.save_model("trained_model_id.bin")