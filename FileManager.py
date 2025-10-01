import os, logging, json
import shutil
from MongoDBManager import MongoDBManager
from bson import ObjectId

class FileManager():
    def __init__(self):  
        self.l_mongodb = MongoDBManager("audios_mongo")
        self.local_salvo = "C:\\Users\\Kaue\\Desenv\\API-AUDIOS\\uploads"
        self.dict_json = 'audios_db.json'
        
    def save_audio(self, l_objAudio, audios):
        file = os.path.join(self.local_salvo, l_objAudio['filename'])
        audios.save(file)
        result = self.l_mongodb.Insert(l_objAudio)
        logging.info('SUCESSO - ARQUIVO CARREGADO COM SUCESSO', 'guid:', result.inserted_id)
        return str(result.inserted_id)

    def get_audio(self, guid):
        return self.l_mongodb.Get(ObjectId(guid))
    
    def delete_audio(self, l_guidFile):
        result = self.l_mongodb.Remove(ObjectId(l_guidFile['_id']))
        file_delete = os.path.join(self.local_salvo, l_guidFile['filename'])
        os.remove(file_delete)
        logging.info('SUCESSO - ARQUIVO REMOVIDO COM ÊXITO')
        
    
    def list_audio(self):
        return self.l_mongodb.List()

    def update_audio(self, l_audio, audios):
        old_filename = l_audio['filename']
        old_file = os.path.join(self.local_salvo, old_filename)
        if os.path.exists(old_file):
            os.remove(old_file)
            logging.info('SUCESSO - ARQUIVO EXCLUÍDO COM ÊXITO')

        l_mongo_update = {
            "filename": audios.filename,
            "create_at": l_audio['create_at']
        }

        result = self.l_mongodb.Update(ObjectId(l_audio['_id']), l_mongo_update)
        new_file = os.path.join(self.local_salvo, audios.filename)
        audios.save(new_file)
        logging.info('SUCESSO - ARQUIVO ALTERADO COM EXITO')
        return str(result.modified_count)
    




            

            
    