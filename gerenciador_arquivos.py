import os, logging, json

class GerenciadorArquivos():
    def __init__(self, local_salvo, dict_json):  
        self.local_salvo = local_salvo
        self.dict_json = dict_json
        
        if not os.path.exists(local_salvo):
            os.makedirs(local_salvo)
        self.audios_db = self.carregar_db()

    def carregar_db(self):
        if os.path.exists(self.dict_json):
            with open(self.dict_json, 'r') as arquivo_json:
                return json.load(arquivo_json)
        return {} ### criei o dicionário audios_db
    def atualizar_db(self):
        with open('audios_db.json','w') as arquivo_json:
            json.dump(self.audios_db, arquivo_json, indent=4)
        logging.info('SUCESSO - BANCO DE DADOS ATUALIZADO COM SUCESSO')

    def salvar_audio(self, guid, audios):
        filename = f"{guid}_{audios.filename}"
        audios.save(os.path.join(self.local_salvo, filename))
        self.audios_db[guid] = filename
        self.atualizar_db()
        logging.info('SUCESSO - ARQUIVO CARREGADO COM SUCESSO')

    def obter_audio(self, guid):
        return self.audios_db.get(guid)
    
    def delete_audio(self, guid):
        filename = self.audios_db.pop(guid, None)
        os.remove(os.path.join(self.local_salvo,filename))
        self.atualizar_db()
        logging.info('SUCESSO - ARQUIVO REMOVIDO COM ÊXITO')
        
    
    def listar_audio(self):
        return [{'guid':guid, 'filename': filename} for guid, filename in self.audios_db.items()]

    def update_audio(self, guid, novo_guid, audios):
        final_guid = guid 
        if novo_guid and novo_guid != guid: 
            if novo_guid in self.audios_db:
                logging.info('ERRO - GUID JÁ EXISTENTE')
                return None 
        self.audios_db[novo_guid] = self.audios_db.pop(guid)
        logging.info('SUCESSO - audios_db ATUALIZADO COM SUCESSO')  

        antigo_filename = self.audios_db.get(final_guid)
        if antigo_filename:
            antigo_arquivo = os.path.join(self.local_salvo, antigo_filename)
            if os.path.exists(antigo_arquivo):
                os.remove(antigo_arquivo)
                logging.info('SUCESSO - ARQUIVO EXCLUÍDO COM ÊXITO')

        final_guid = novo_guid
        novo_filename = f"{final_guid}_{audios.filename}"
        audios.save(os.path.join(self.local_salvo, novo_filename))
        self.audios_db[final_guid] = novo_filename
        self.atualizar_db()
        logging.info('SUCESSO - ARQUIVO ALTERADO COM EXITO')
        return final_guid
    




            

            
    