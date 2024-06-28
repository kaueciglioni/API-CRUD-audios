### NOVAS ATUALIZAÇÕES NO CÓDIGO
# não operar em memória - operar em disco
# log - feito
# classe para manipulação de arquivo

from flask import  Flask, request, jsonify, send_from_directory
import logging
from gerenciador_arquivos import GerenciadorArquivos 

app = Flask(__name__)

local_salvo = '/home/kaue/voxProjects/projeto_Teste/uploads'
dict_json = 'audios_db.json'

gerenciador_de_arquivo = GerenciadorArquivos(local_salvo, dict_json)

logging.basicConfig(filename='info.log',filemode='w', level=logging.INFO,
                     format='%(asctime)s - %(levelname)s - %(message)s')

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

    if guid in gerenciador_de_arquivo.audios_db: 
        logging.info('ERRO - GUID JÁ EXISTENTE')
        return {'ERRO': 'guid JA EXISTENTE'}, 400

    gerenciador_de_arquivo.salvar_audio(guid, audios)
    return {'MENSAGEM': 'AUDIO CARREGADO COM SUCESSO','guid': guid}, 201
    
#2- rota para exibir o guid solicitado que vai trazer o audio associado ao guid 
@app.route('/Home/<string:guid>', methods=['GET'])
def searchguid(guid):
    filename = gerenciador_de_arquivo.obter_audio(guid)
    if guid not in gerenciador_de_arquivo.audios_db:
        logging.error('ERRO - GUID não existente')
        return {'ERRO': 'guid NÃO EXISTENTE'}, 400
    logging.info('SUCESSO - AUDIO CARREGADO E PRONTO PARA VISUALIZAÇÃO')
    return send_from_directory(local_salvo, filename)

#3- procurar o guid e deletar o audio e o guid
@app.route('/Home/delete/<string:guid>', methods=['DELETE'])
def delete(guid):
    if not guid in gerenciador_de_arquivo.audios_db:
        logging.error('GUID não existente')
        return {'ERRO': 'guid NÃO EXISTENTE'}, 400
    gerenciador_de_arquivo.delete_audio(guid)
    return {'SUCESSO': 'ARQUIVO REMOVIDO COM EXITO'}, 200

#4- rota para mostrar todos os guids que foram incluidos, em formato de list, com todos os arquivos adicionados
@app.route('/Home/list', methods=['GET'])
def list():
    audio_list = gerenciador_de_arquivo.listar_audio()
    logging.info('SUCESSO - TODOS OS ARQUIVOS FORAM EXIBIDOS CORRETAMENTE')
    return jsonify(audio_list)

#5- rota para atualizar de guids pelo id com a alteração do arquivo
@app.route('/Home/update/<string:guid>', methods=['PUT'])
def update(guid):
    if 'audios' not in request.files or not request.files['audios']:
        logging.error('Nenhum arquivo enviado na requisição')
        return {'ERRO': 'AUDIO NÃO ENVIADO'}, 400
    
    if guid not in gerenciador_de_arquivo.audios_db:
        logging.error('GUID não existente')
        return {'ERRO': 'guid NÃO EXISTENTE'}, 400
    
    novo_guid = request.form.get('guid')
    final_guid = gerenciador_de_arquivo.update_audio(guid, novo_guid, request.files['audios'])
    return {'SUCESSO': 'ARQUIVO ALTERADO COM ÊXITO', 'guid': final_guid}, 200 

#6- nominar a porta utilizada e o diretório para a requisição da API
if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)


