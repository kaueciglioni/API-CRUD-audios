
# não operar em memória - operar em disco
# log - feito
# classe para manipulação de arquivo


from flask import  Flask, request, jsonify, send_from_directory
import os, logging, json

app = Flask(__name__)

LOCAL_SALVO = '/home/kaue/voxProjects/projeto_Teste/uploads'
dict_json = 'audios_db.json'

logging.basicConfig(filename='LOG-API-CRUD.log',filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

## -  Imports
## - Instancia FLASK
## - Váriaveis compostas
## - Config de LOGS

if not os.path.exists(LOCAL_SALVO):
    os.makedirs(LOCAL_SALVO)

if os.path.exists(dict_json):
    with open(dict_json, 'r') as arquivo_json:
        audios_db = json.load(arquivo_json)
else:
    audios_db = {}

##def carregar_para_dicionario(dict_json):
  ##  with open(audios_db.json,'r') as arquivo_json:
    ##    json.load(arquivo_json)
    ##return {'SUCESSO': 'ARQUIVO EXPORTADO COM SUCESSO'} 

## audios_db = carregar_para_dicionario(dict_json)

def atualizar_db():
    with open('audios_db.json','w') as arquivo_json:
      json.dump(audios_db, arquivo_json, indent=4)
      logging.info('SUCESSO - BANCO DE DADOS ATUALIZADO COM SUCESSO')

                  
############## CRIANDO O CRUD ################

#0- home page da api para a biblioteca de áudio
@app.route('/Home', methods=['GET'])
def inicio():
    logging.info('SUCESSO - GET REALIZADO PARA A PÁGINA INICIAL')
    return 'BEM VINDO PARA A PAGINA INICIAL, PARA ADICIONAR ARQUIVO, USE:  /Home/create '

#1- Subir arquivo do áudio e informar qual o guid
@app.route('/Home/create', methods=['POST'])
def create():

    if 'audios' not in request.files or not request.files['audios']:
        logging.error('ERRO - NENHUM ARQUIVO ENVIADO NA REQUISIÇÃO')
        return {'ERROR': 'NENHUM ARQUIVO ENCONTRADO'}, 400
    
    audios = request.files['audios']
    guid = request.form.get('guid')

    if not guid:
        logging.error('ERRO - GUID NÃO INSERIDA')
        return {'ERRO': 'GUID NÃO INSERIDA'}, 400
    
    
    if guid in audios_db: 
        logging.info('ERRO - GUID JÁ EXISTENTE')
        return {'ERRO': 'guid JA EXISTENTE'}, 400
    
    filename = f"{guid}_{audios.filename}"
    audios.save(os.path.join(LOCAL_SALVO, filename))
    audios_db[guid] = filename

    atualizar_db()
    
    logging.info('SUCESSO - ARQUIVO CARREGADO COM SUCESSO')
    return {'MENSAGEM': 'AUDIO CARREGADO COM SUCESSO','guid': guid}, 201




#2- rota para exibir o guid solicitado que vai trazer o audio associado ao guid 
@app.route('/Home/<string:guid>', methods=['GET'])
def searchguid(guid):
    if guid not in audios_db:
        logging.error('ERRO - GUID não existente')
        return {'ERRO': 'guid NÃO EXISTENTE'}, 400
    
    filename = audios_db[guid]
    logging.info('SUCESSO - AUDIO CARREGADO E PRONTO PARA VISUALIZAÇÃOF')
    return send_from_directory(LOCAL_SALVO,filename)

#3- procurar o guid e deletar o audio e o guid
@app.route('/Home/delete/<string:guid>', methods=['DELETE'])
def delete(guid):
    if not guid in audios_db:
        logging.error('GUID não existente')
        return {'ERRO': 'guid NÃO EXISTENTE'}, 400
    filename = audios_db.pop(guid)
    os.remove(os.path.join(LOCAL_SALVO,filename))

    atualizar_db()

    logging.info('SUCESSO - ARQUIVO CARREGAOD COM SUCESSO')
    return {'SUCESSO': 'ARQUIVO REMOVIDO COM EXITO'}, 200

#4- rota para mostrar todos os guids que foram incluidos, em formato de list, com todos os arquivos adicionados
@app.route('/Home/list', methods=['GET'])
def list():
    audio_list = [{'guid':guid,'filename':filename} for guid, filename in audios_db.items()]
    logging.info('SUCESSO - TODOS OS ARQUIVOS FORAM EXIBIDOS CORRETAMENTE')
    return jsonify(audio_list)



#5- rota para atualizar de guids pelo id com a alteração do arquivo
@app.route('/Home/update/<string:guid>', methods=['PUT'])
def update(guid):
    if 'audios' not in request.files:
        logging.error('Nenhum arquivo enviado na requisição')
        return {'ERRO': 'AUDIO NÃO ENVIADO'}, 400
    
    if guid not in audios_db:
        logging.error('GUID não existente')
        return {'ERRO': 'guid NÃO EXISTENTE'}, 400
    
    novo_guid = request.form.get('guid')

    final_guid = guid 
    if novo_guid and novo_guid != guid: 
        if novo_guid in audios_db:
            logging.info('ERRO - GUID JÁ EXISTENTE')
            return {'ERRO': 'guid JÁ EXISTENTE'}, 400
        
        audios_db[novo_guid] = audios_db.pop(guid)
        final_guid = novo_guid
        logging.info('SUCESSO - audios_db ATUALIZADO COM SUCESSO')  
    
    audios = request.files['audios']
    
    antigo_filename = audios_db.get(final_guid)
    if antigo_filename:
        antigo_arquivo = os.path.join(LOCAL_SALVO, antigo_filename)
        if os.path.exists(antigo_arquivo):
            os.remove(antigo_arquivo)
            logging.info('SUCESSO - ARQUIVO EXCLUÍDO COM ÊXITO')

    novo_filename = f"{final_guid}_{audios.filename}"
    audios.save(os.path.join(LOCAL_SALVO, novo_filename))
    audios_db[final_guid] = novo_filename

    atualizar_db()

    logging.info('SUCESSO - ARQUIVO ALTERADO COM EXITO')
    return {'SUCESSO': 'ARQUIVO ALTERADO COM EXITO', 'guid': final_guid}, 200

#7- nominar a porta utilizada e o diretório para a requisição da API
if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)


