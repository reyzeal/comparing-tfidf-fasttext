import pymongo
import requests
from pymongo import UpdateOne

from web import socketio


def retrieve_from_web():
    socketio.emit("")
    r = requests.get("http://eprints.upnyk.ac.id/cgi/search/archive/advanced/export_eprints_JSON.js?dataset=archive"
                     "&screen=Search&_action_export=1&output=JSON&exp=0%7C1%7C-date%2Fcreators_name%2Ftitle%7Carchive"
                     "%7C-%7Cdepartment%3Adepartment%3AALL%3AIN%3AINFORMATIKA%7Ctype%3Atype%3AANY%3AEQ%3Athesis%7C"
                     "-%7Ceprint_status%3Aeprint_status%3AANY%3AEQ%3Aarchive%7Cmetadata_visibility"
                     "%3Ametadata_visibility%3AANY%3AEQ%3Ashow&n=&cache=152949")
    data = r.json()
    result = []
    for i in data:
        result.append(UpdateOne({
            '_id': i['eprintid'],
        }, {
            '$setOnInsert': {
                '_id': i['eprintid'],
                'data': i,
            }
        }, upsert=True))
    client = pymongo.MongoClient("localhost", 27017)
    db = client['skripsi']
    collection = db["documents"]
    collection.bulk_write(result)
    return data
