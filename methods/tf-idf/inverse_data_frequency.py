"""
    Term Frequency
    menghitung frequency dari kata
"""
import math


def inverse_data_frequency(documents):
    idf = {}
    for doc in documents:
        for word, value in doc.items():
            if value > 0:
                idf[word] = 1+idf[word] if word in idf else 1
    total = len(documents)
    for word, count in idf.items():
        idf[word] = math.log10(float(total) / count)
    return idf


if __name__ == '__main__':
    import preprocessing.__index
    from term_frequency import term_frequency
    test = [
        "Saya menyukai cabai dan paprika",
        "Petani cabai sedang kewalahan mencari pupuk",
        "Buruh tani beralih menjadi kuli bangunan"
    ]
    for i in test:
        preprocessed, _ = preprocessing.__index.preprocessing(i)
        tf = term_frequency(preprocessed, ['suka', 'cabai'])
    idf = inverse_data_frequency([tf])
    print(tf, idf)
