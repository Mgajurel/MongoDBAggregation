from gc import collect
from pymongo import MongoClient
from random import randint
from pprint import pprint as pp
import logging as log

SERVER_HOST_MAP = {'local': 'localhost:27017',
                   'Server1': "10.45.3.1:27017",
                   'Server2': "10.45.3.2:27017",
                   'Server3': "10.45.3.3:27017"}


def connect_client(host_port):
    """connects to a mongo server

    Args:
        host_port (str): hostname:port

    Returns:
        object: Mongo Client
    """
    client = MongoClient(host_port)
    return client


def alligator():
    """Creats a pipeline for mongo aggregation

    Returns:
        list: list of pipelines
    """
    pipeline1 = {'$match': {'items.name': {'$in': ['bagpack', 'laptop']},
                            'purchaseMethod': 'Online', 'customer.age': {'$lt': 30}}}

    pipeline2 = {'$unwind': '$items'}

    pipeline3 = {'$group': {
        '_id': '$customer',
        'totalPurchase': {'$sum': {'$multiply': ['$items.price', '$items.quantity']}}}}

    pipeline4 = {'$project': {'totalPurchase': 1, 'customer': '$_id', '_id': 0, 'environment':
                              {'$switch': {'branches': [
                                  {'case': {
                                      '$gt': ['$totalPurchase', 5000]}, 'then': 'Server1'},
                                  {'case': {
                                      '$lt': ['$totalPurchase', 2000]}, 'then': 'Server3'},
                              ],
                                  'default': 'Server2'
                              }}}}

    pipeline5 = {'$group': {
        '_id': '$environment', 'data': {'$push': '$$ROOT'}}}

    return [pipeline1, pipeline2, pipeline3, pipeline4, pipeline5]


def write_to_servers(documents):
    """wites the documents to their respective server

    Args:
        documents (mongo DB cursor): cusrsor to mongo documents
    """
    for doc in documents:
        db = connect_client(SERVER_HOST_MAP.get(doc.get('_id')))[
            doc.get('_id')]

        db.aggregated_result.insert_many(doc.get('data'))


if __name__ == '__main__':
    client = connect_client(SERVER_HOST_MAP.get('local'))
    db = client['supply']
    collection = db.sales
    documents = collection.aggregate(alligator())
    try:
        write_to_servers(documents)
    except Exception as E:
        log.error('Failed to Insert, {}', E)
    else:
        print('Database Creation Successfull')
