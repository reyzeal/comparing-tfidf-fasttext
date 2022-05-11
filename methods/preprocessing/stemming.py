"""
    Tahap V

    Stemming adalah mengubah setiap kata menjadi bentuk kata dasarnya dengan membuang imbuhan awal / akhir.

"""
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


def stemming(arr):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    return [stemmer.stem(text) for text in arr]
