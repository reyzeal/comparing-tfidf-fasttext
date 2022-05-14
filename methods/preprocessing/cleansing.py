"""
    Tahap I

    Cleansing adalah tahapan menghilangkan whitespace yang tidak diinginkan
"""
import re




def cleansing(text, verbose=False):
    text = re.sub('(\n|\r|\\n|\\r|\t|\\t)', ' ', text)
    if verbose:
        print(text)
    text = re.sub('[^a-zA-Z ]', '', text)
    if verbose:
        print(text)
    text = re.sub('\s{2,}', ' ', text)
    if verbose:
        print(text)
    text = re.sub('^\s+|\s+$', '', text)
    if verbose:
        print(text)
    return text


if __name__ == "__main__":
    from preprocessing import preprocessing
    x = preprocessing("ANALISIS SENTIMEN KEBIJAKAN PEMERINTAH DALAM PENANGANAN\r\nPANDEMI CORONAVIRUS DISEASE 2019 (COVID-19) BERDASARKAN OPINI\r\nMASYARAKAT PADA MEDIA SOSIAL TWITTER MENGGUNAKAN METODE\r\nSUPPORT VECTOR MACHINE (SVM)")
    print(x)
    # cleansing(, True)