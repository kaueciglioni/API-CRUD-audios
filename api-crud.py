from flask import  Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = '/home/kaue/voxProjects/projeto_Teste/uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

audios_db = {}

#### CRIANDO O CRUD ####
#0- home page da api para a biblioteca de áudio
@app.route('/Home', methods=['GET'])
def inicio():
    return 'BEM VINDO PARA A PAGINA INICIAL, PARA ADICIONAR ARQUIVO, USE:  /Home/create '

#1- Subir arquivo do áudio e informar qual o guid
@app.route('/Home/create', methods=['POST'])
def create():
    if 'audios' not in request.files:
        return {'ERROR': 'NENHUM ARQUIVO ENCONTRADO'}, 400
    
    audios = request.files['audios']
    guid = request.form.get('guid')

    if not guid:
        return {'ERRO': 'guid NÃO EXISTENTE'}, 400
    
    if guid in audios_db: 
        return {'ERRO': 'guid JA EXISTENTE'}, 400
    
    filename = f"{guid}_{audios.filename}"
    audios.save(os.path.join(UPLOAD_FOLDER, filename))
    audios_db[guid] = filename
    return {'MENSAGEM': 'AUDIO CARREGADO COM SUCESSO','guid': guid}, 201



#2- rota para exibir o guid solicitado que vai trazer o audio associado ao guid 
@app.route('/Home/<string:guid>', methods=['GET'])
def searchguid(guid):
    if guid not in audios_db:
        return {'ERRO': 'guid NÃO EXISTENTE'}, 400
    
    filename = audios_db[guid]
    return send_from_directory(UPLOAD_FOLDER,filename)

#3- procurar o guid e deletar o audio e o guid
@app.route('/Home/delete/<string:guid>', methods=['DELETE'])
def delete(guid):
    if not guid in audios_db:
        return {'ERRO': 'guid NÃO EXISTENTE'}, 400
    filename = audios_db.pop(guid)
    os.remove(os.path.join(UPLOAD_FOLDER,filename))
    return {'SUCESSO': 'ARQUIVO REMOVIDO COM EXITO'}, 200

#3- rota para mostrar todos os guids que foram incluidos, em formato de list, com todos os arquivos adicionados
@app.route('/Home/list', methods=['GET'])
def list():
    audio_list = [{'guid':guid,'filename':filename} for guid, filename in audios_db.items()]
    return jsonify(audio_list)



#4- rota para atualizar de guids pelo id com a alteração do arquivo
@app.route('/Home/update/<string:guid>', methods=['PUT'])
def update(guid):
    if 'audios' not in request.files:
        return {'ERRO': 'AUDIO NÃO ENVIADO'}, 400
    
    if guid not in audios_db:
        return {'ERRO': 'guid NÃO EXISTENTE'}, 400
    
    novo_guid = request.form.get('guid')

    final_guid = guid 
    if novo_guid and novo_guid != guid: 
        if novo_guid in audios_db:
            return {'ERRO': 'guid JÁ EXISTENTE'}, 400
        
        
        audios_db[novo_guid] = audios_db.pop(guid)
        final_guid = novo_guid  
    
    audios = request.files['audios']
    
    antigo_filename = audios_db.get(final_guid)
    if antigo_filename:
        antigo_arquivo = os.path.join(UPLOAD_FOLDER, antigo_filename)
        if os.path.exists(antigo_arquivo):
            os.remove(antigo_arquivo)

    novo_filename = f"{final_guid}_{audios.filename}"
    audios.save(os.path.join(UPLOAD_FOLDER, novo_filename))
    audios_db[final_guid] = novo_filename
    return {'SUCESSO': 'ARQUIVO ALTERADO COM EXITO', 'guid': final_guid}, 200

#6- nominar a porta utilziada e o diretório para a requisição da API
if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)


