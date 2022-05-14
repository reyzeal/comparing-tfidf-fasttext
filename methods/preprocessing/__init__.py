from preprocessing.cleansing import cleansing
from preprocessing.case_folding import casefolding
from preprocessing.tokenizing import tokenisasi
from preprocessing.stopword import stopword
from preprocessing.stemming import stemming

'''

Preprocessing
1. Cleansing = replace \n \r \n\r space chars
2. CaseFolding = lowercase
3. Tokenisasi = str to arr
4. Stopword = remove unused word
5. Stemming = kata dasar

:return str, dict
'''


def preprocessing(text):
    result = {'cleansing': cleansing(text), 'casefolding': '', 'tokenisasi': '', 'stopword': '', 'stemming': ''}

    result['casefolding'] = casefolding(result['cleansing'])
    result['tokenisasi'] = tokenisasi(result['casefolding'])
    result['stopword'] = stopword(result['tokenisasi'])
    result['stemming'] = stemming(result['stopword'])

    return result['stemming'], result


if __name__ == "__main__":
    test = '''SISTEM PENDUKUNG KEPUTUSAN PENILAIAN KARYAWAN BERPRESTASI
BERDASARKAN KINERJA BERBASIS WEB DENGAN METODE ANALYTICAL
HIERARCHY PROSES ( AHP )
( Studi kasus pada PT Anindya Mitra Internasional Yogyakarta )'''

    print(preprocessing(test))