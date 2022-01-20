# This Script is used to randomly assign Server1, Server2, or Server 3
# to a field environment for each document in out collection sales


from time import sleep


def update_collection():
    from pymongo import MongoClient
    import random

    client = MongoClient('localhost', 27017)

    # listsing available dbs
    # print (client.list_database_names())

    db = client['test']

    # listsing available collections
    # print(db.list_collection_names())

    server_names = ['Server1', 'Server2', 'Server3']
    sales = db.sales

    documents = sales.find()
    for document in documents:
        _id = document['_id']
        sales.update_one(
            {"_id": _id}, {'$set': {'environment': random.choice(server_names)}})


if __name__ == '__main__':
    print ("Are you sure you want to run this script, it has an update being run? (Y/N)")
    choice = input()
    if choice == 'Y':
        print("Updating.....")
        update_collection()
    else:
        print("Exiting.....")
        sleep(1)
        exit(0)
