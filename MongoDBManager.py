import pymongo
import config


class MongoDBManager:
    def __init__(self, db_name):
        self.uri = config.MONGODB_URI
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client[db_name]  # seleciona o banco

    def Insert(self, audio_data):
        l_colection = self.db["audios"]  # pega a coleção "audios"
        result = l_colection.insert_one(audio_data)
        return result
    
    def Remove(self, audio_id):
        l_colection = self.db["audios"]
        result = l_colection.delete_one({"_id": audio_id})  
        return result.deleted_count
    
    def Update(self, audio_id, update_data):
        l_colection = self.db["audios"]
        result = l_colection.update_one({"_id": audio_id}, {"$set": update_data})
        return result
    
    def Get(self, audio_id):
        l_colection = self.db["audios"]
        result = l_colection.find_one({"_id": audio_id})
        return result
    
    def List(self):
        l_colection = self.db["audios"]
        results = l_colection.find()

        l_dict = {}
        for doc in results:
            doc_id = str(doc["_id"])
            del doc["_id"]  # remove o _id duplicado
            l_dict[doc_id] = doc
        
        return l_dict