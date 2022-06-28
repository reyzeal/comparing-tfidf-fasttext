import pymongo

'''
    Retrieve from DB
    
    :return list of dict
'''


def retrieve(id=None):
    client = pymongo.MongoClient("localhost", 27017)
    x = client['skripsi']
    if id is None:
        data = [i for i in x.get_collection('documents').find()]
    else:
        data = x.get_collection('documents').find_one({'_id': id})
    return data

def retrieveByIndex(id=None):
    client = pymongo.MongoClient("localhost", 27017)
    x = client['skripsi']
    if id is None:
        data = [i for i in x.get_collection('documents').find()]
    else:
        data = x.get_collection('documents').find_one({'id': id})
    return data


def update(id, data):
    client = pymongo.MongoClient("localhost", 27017)
    x = client['skripsi']
    collection = x.get_collection("documents")
    collection.update_one({'_id': id}, {
        "$set": data
    })


if __name__ == "__main__":
    data = retrieve()
    for i in data:
        update(i['_id'], {'preprocessed': None})
    print()
