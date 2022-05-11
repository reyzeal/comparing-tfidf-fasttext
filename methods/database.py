import pymongo

'''
    Retrieve from DB
    
    :return list of dict
'''


def retrieve():
    client = pymongo.MongoClient("localhost", 27017)
    x = client['skripsi']
    data = [i['data'] for i in x.get_collection('documents').find()]
    return data


if __name__ == "__main__":
    print(retrieve())
