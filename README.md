# API-CRUD-audios

Claro, aqui está uma descrição simples do projeto e um README para orientá-lo sobre como usá-lo:

### Descrição do Projeto

Este projeto é uma API Flask para upload e atualização de arquivos de áudio. Ele permite que você envie arquivos de áudio associados a identificadores únicos (GUIDs). A API permite atualizar o áudio existente e, opcionalmente, alterar o GUID associado ao arquivo.

### Estrutura do Projeto

- `app.py`: Arquivo principal contendo a lógica da API.
- `UPLOAD_FOLDER`: Diretório onde os arquivos de áudio são armazenados.
- `audios_db`: Dicionário em memória para mapear GUIDs aos nomes dos arquivos de áudio.

### README

```markdown
# Audio Upload and Update API

Esta API permite o upload e a atualização de arquivos de áudio associados a identificadores únicos (GUIDs). 

## Requisitos

- Python 3.6 ou superior
- Flask

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/audio-upload-api.git
cd audio-upload-api
```

2. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
pip install flask
```

## Configuração

1. Atualize a variável `UPLOAD_FOLDER` no arquivo `app.py` para o diretório onde deseja armazenar os arquivos de áudio:

```python
UPLOAD_FOLDER = '/caminho/para/seu/diretorio/uploads'
```

2. Inicie o servidor Flask:

```bash
python app.py
```

## Uso

### Endpoint: Upload e Atualização de Áudio

- **URL:** `/Home/update/<guid>`
- **Método:** `PUT`

#### Parâmetros

- **Path Parameter:**
  - `guid`: O identificador único do áudio que deseja atualizar.

- **Form Data:**
  - `audios`: O novo arquivo de áudio a ser carregado.
  - `novo_guid` (opcional): O novo GUID para substituir o existente.

#### Exemplo de Requisição com Postman

1. Defina o método como `PUT`.
2. Use a URL `http://localhost:5000/Home/update/<guid>`, substituindo `<guid>` pelo GUID atual do áudio.
3. Na aba `Body`, selecione `form-data` e adicione os seguintes campos:
   - `audios`: Selecione o arquivo de áudio.
   - `novo_guid` (opcional): Insira o novo GUID desejado.

#### Exemplo de Configuração no Postman

- **URL:** `http://localhost:5000/Home/update/12345`
- **Body (form-data):**
  - `Key`: `audios` | `Type`: File | `Value`: Selecione o arquivo de áudio
  - `Key`: `novo_guid` | `Type`: Text | `Value`: novo_guid (se necessário)

#### Respostas

- **200 OK:** Se o áudio foi atualizado com sucesso.
  ```json
  {
    "SUCESSO": "ARQUIVO ALTERADO COM EXITO",
    "guid": "final_guid"
  }
  ```
- **400 Bad Request:** Se ocorrer um erro (ex: áudio não enviado, GUID não existente, novo GUID já existente).

## Contribuição

1. Faça um fork do projeto.
2. Crie uma nova branch (`git checkout -b feature/sua-feature`).
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova feature'`).
4. Faça push para a branch (`git push origin feature/sua-feature`).
5. Crie um novo Pull Request.



### Notas Adicionais

- Certifique-se de que o diretório especificado em `UPLOAD_FOLDER` exista e tenha permissões adequadas para leitura e escrita.
- Para testar a API, você pode usar ferramentas como Postman, cURL ou escrever scripts em Python para enviar requisições HTTP.

Com este README, você deve ter uma boa base para configurar e usar o projeto. Certifique-se de ajustar o conteúdo conforme necessário para o seu ambiente específico e quaisquer outras especificidades do seu projeto.
