from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import Config

app = Flask(__name__)

client = MongoClient(Config.MONGO_URI, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["mydatabase"]
collection = db["mycollection"]


@app.route('/', methods=['GET'])
def get():
    result = collection.find({})
    data = {}
    for item in result:
        data[item['key']] = item['value']
    return jsonify(data)


@app.route('/', methods=['POST'])
def create():
    req_data = request.get_json()
    if 'key' not in req_data:
        return jsonify({'error': 'Key is missing'}), 400
    key = req_data.get('key')
    value = req_data.get('value')
    collection.insert_one({'key': key, 'value': value})
    return jsonify({'message': 'Key-Value pair created successfully'})


@app.route('/', methods=['PUT'])
def update():
    req_data = request.get_json()
    if 'key' not in req_data:
        return jsonify({'error': 'Key is missing'}), 400
    key = req_data.get('key')
    value = req_data.get('value')
    result = collection.update_one({'key': key}, {'$set': {'value': value}})
    if result.modified_count > 0:
        return jsonify({'message': 'Value updated successfully'})
    else:
        return jsonify({'error': 'Key not found'}), 404


@app.route('/alarm', methods=['POST'])
def handle_alarm():
    print("Received alarm!")
    return jsonify({'message': 'Alarm received'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
