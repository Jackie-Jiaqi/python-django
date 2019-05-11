from pymongo import MongoClient
import pymongo


class MongoConnect:
    def __init__(self, address="localhost", port=27017):
        self.address = address
        self.port = port
        self.connection = MongoClient(address, port)

    def auth(self, dbname, username, password):
        try:
            self.connection[dbname].authenticate(username, password)
            return 1
        except Exception:
            return "Authentication Failed"

    def find_one(self, dbname, collection):
        try:
            return list(self.connection[dbname][collection].find_one({}, {'_id': 0}))
        except Exception:
            return "Records Not Found"

    def data_list(self, dbname, collection, column, order, start_point, number):
        if order == 'asc':
            direction = pymongo.ASCENDING
        else:
            direction = pymongo.DESCENDING
        return list(self.connection[dbname][collection].find({}, {'_id': 0}).sort(column, direction).skip(start_point).limit(number))

    #def column_list(self, dbname, collection):

