"""
    Tahap I

    Cleansing adalah tahapan menghilangkan whitespace yang tidak diinginkan
"""
import re


def cleansing(text):
    text = re.sub(r'(\n|\r|\\n|\\r)', ' ', text)
    text = re.sub(r'\s{2,}',' ', text)
    return text
