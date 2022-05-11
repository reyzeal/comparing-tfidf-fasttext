from pprint import pprint
from database import retrieve
from preprocessing.__index import preprocessing

if __name__ == '__main__':
    data = retrieve()

    for i in data:
        preprocessed = preprocessing(i['title'])
        pprint(preprocessed)
        print(i['title'])
        break
