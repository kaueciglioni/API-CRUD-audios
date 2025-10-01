from flask import  Flask, request, jsonify, send_from_directory, current_app
import logging, uuid
from datetime import datetime
from FileManager import FileManager 
from Audio import Audio
from uuid import uuid4
import config


app = Flask(__name__)
app.config.from_mapping(
    UPLOAD_FOLDER=config.UPLOAD_FOLDER
)

l_fileManager = FileManager()

logging.basicConfig(filename='debug.log',filemode='w', level=logging.DEBUG,
                     format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/Home/create', methods=['POST'])
def create():
    if 'audios' not in request.files or not request.files['audios']:
        logging.error('ERRO - NENHUM ARQUIVO ENVIADO NA REQUISIÇÃO')
        return {'ERROR': 'NENHUM ARQUIVO ENCONTRADO'}, 400
    
    audios = request.files['audios']

    l_objAudio = Audio(
        filename= audios.filename,
        create_at= datetime.now().isoformat())

    _id = l_fileManager.save_audio(l_objAudio, audios)
    return {'SUCESS': 'AUDIO CARREGADO COM SUCESSO', 'guid': _id}, 201

@app.route('/Home/<string:guid>', methods=['GET'])
def searchguid(guid):
    l_object = l_fileManager.get_audio(guid)
    if not l_object:
        logging.error('ERROR - GUID não existente')
        return {'ERROR': 'guid NÃO EXISTENTE'}, 400
    logging.debug('SUCESS - AUDIO CARREGADO E PRONTO PARA VISUALIZAÇÃO')
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], l_object['filename'])

@app.route('/Home/delete/<string:guid>', methods=['DELETE'])
def delete(guid):
    l_guidFile = l_fileManager.get_audio(guid)
    if not l_guidFile:
        logging.error('GUID não existente')
        return {'ERROR': 'guid NÃO EXISTENTE'}, 400
    l_fileManager.delete_audio(l_guidFile)
    return {'SUCESS': 'ARQUIVO REMOVIDO COM EXITO'}, 200

@app.route('/Home/list', methods=['GET'])
def list():
    audio_list = l_fileManager.list_audio()
    logging.debug('SUCESS - TODOS OS ARQUIVOS FORAM EXIBIDOS CORRETAMENTE')
    return jsonify(audio_list)

@app.route('/Home/update/<string:guid>', methods=['PUT'])
def update(guid):
    if 'audios' not in request.files or not request.files['audios']:
        logging.error('Nenhum arquivo enviado na requisição')
        return {'ERROR': 'AUDIO NÃO ENVIADO'}, 400

    l_guidFile = l_fileManager.get_audio(guid)
    if not l_guidFile:
        logging.error('GUID não existente')
        return {'ERROR': 'guid NÃO EXISTENTE'}, 400
    
    final_file = l_fileManager.update_audio(l_guidFile, request.files['audios'])
    return {'SUCESS': 'ARQUIVO ALTERADO COM ÊXITO'}, 200 

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)


