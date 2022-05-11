"""
    Tahap III

    Case Folding digunakan unutk mengubah text huruf besar ke huruf kecil.

"""
import re


def cleansing(text):
    text = re.sub(r'(\n|\r|\\n|\\r)', ' ', text)
    text = re.sub(r'\s{2,}',' ', text)
    return text
