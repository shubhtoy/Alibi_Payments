from pymongo import MongoClient
import pymongo
from pymongo import MongoClient


def get_database(name):

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://shubh:shubh2003@paymentdetails.dvub8on.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[name]


# This is added so that many files can reuse the function get_database()


# Get the database
item_1 = {
    "item_name": "Blender",
    "max_discount": "10%",
    "batch_number": "RR450020FRG",
    "price": 340,
    "category": "kitchen appliance",
}


def initialize_database(name, collection_name):
    db = get_database(name)
    collection = db[collection_name]
    return collection


# collection_name = dbname["Alibi_Payments"]
# collection_name.insert_one(item_1)


class Database:
    def __init__(self, dbname, collection_name):
        self.dbname = dbname
        self.collection_name = collection_name
        self.collection = initialize_database(dbname, collection_name)

    def insert_one(self, data):
        self.collection.insert_one(data)

    def insert_many(self, data):
        self.collection.insert_many(data)

    def find(self):
        return self.collection

    def find_all(self, field):
        return self.collection.find({}, {field: 1, "_id": 0})

    def find_one(self, query):
        return self.collection.find(query)

    def find_many(self, query):
        return self.collection.find(query)

    def update_one(self, query, data):
        self.collection.update_one(query, data)

    def update_many(self, query, data):
        self.collection.update_many(query, data)

    def delete_one(self, query):
        self.collection.delete_one(query)

    def delete_many(self, query):
        self.collection.delete_many(query)

    def count(self, query):
        return self.collection.count(query)

    def distinct(self, query):
        return self.collection.distinct(query)

    def aggregate(self, query):
        return self.collection.aggregate(query)

    def map_reduce(self, query):
        return self.collection.map_reduce(query)

    def drop(self):
        self.collection.drop()

    def create_index(self, query):
        self.collection.create_index(query)

    def drop_index(self, query):
        self.collection.drop_index(query)

    def drop_indexes(self):
        self.collection.drop_indexes()

    def index_information(self):
        return self.collection.index_information()

    def options(self):
        return self.collection.options()

    def rename(self, new_name):
        self.collection.rename(new_name)

    def distinct(self, query):
        return self.collection.distinct(query)

    def group(self, query):
        return self.collection.group(query)


class Payments(Database):
    def __init__(self, name, collection_name):
        super().__init__(name, collection_name)

    def create_team(self, query):
        super().insert_one(query)

    def update_team(self, query, data):
        super().update_one({"team_name": query}, {"$set": data})

    def get_team(self, query):
        return super().find_one(query)

    def get_all_teams(self):
        return list((super().find_all("team_name")))


# database = Payments("PaymentDetails_test", "Alibi_Payment")
# database.update_team(
#     "CIPHER HUNTERS",
#     {
#         "payment_pending": False,
#         "team_name": "CIPHER HUNTERS",
#         "payment_details": {
#             "entity": {
#                 "acquirer_data": {"auth_code": "766456"},
#                 "amount": 11200,
#                 "amount_refunded": 0,
#                 "amount_transferred": 0,
#                 "bank": None,
#                 "base_amount": 11200,
#                 "captured": True,
#                 "card": {
#                     "emi": False,
#                     "entity": "card",
#                     "id": "card_JzK2soUHXkj0gL",
#                     "international": False,
#                     "issuer": "STCB",
#                     "last4": "2847",
#                     "name": "shubh",
#                     "network": "Visa",
#                     "sub_type": "consumer",
#                     "token_iin": None,
#                     "type": "prepaid",
#                 },
#                 "card_id": "card_JzK2soUHXkj0gL",
#                 "contact": "+919311910111",
#                 "created_at": 1659128387,
#                 "currency": "INR",
#                 "description": "#JzK0DQICbTgt8P",
#                 "email": "rrr@kj.d",
#                 "entity": "payment",
#                 "error_code": None,
#                 "error_description": None,
#                 "error_reason": None,
#                 "error_source": None,
#                 "error_step": None,
#                 "fee": 224,
#                 "fee_bearer": "platform",
#                 "id": "pay_JzK2skrP5zsYZk",
#                 "international": False,
#                 "invoice_id": None,
#                 "method": "card",
#                 "notes": [],
#                 "order_id": "order_JzK0hZI4uVcN7q",
#                 "refund_status": None,
#                 "status": "captured",
#                 "tax": 0,
#                 "vpa": None,
#                 "wallet": None,
#             }
#         },
#     },
# )
