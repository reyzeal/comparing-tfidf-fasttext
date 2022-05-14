import fasttext

from _fasttext import most_similar

model = fasttext.load_model("trained_model_id.bin")
print(most_similar(model, 'yogyakarta', top=10))