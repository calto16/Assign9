from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/todo_db'
mongo = PyMongo(app)
@app.route('/todo', methods=['GET'])
def get_todo_list():
    todos_collection = mongo.db.todos
    todos = todos_collection.find({}, {'_id': 1, 'task': 1})  # Only fetch _id and task fields
    todo_list = []
    for todo in todos:
        if '_id' in todo:  # Check if _id field is present in the document
            todo_list.append({'id': str(todo['_id']), 'task': todo['task']})
    return jsonify(todo_list)

@app.route('/todo', methods=['POST'])
def create_todo():
    todo_data = request.json
    task = todo_data.get('task')
    if task:
        todo_id = str(uuid.uuid4())
        todos_collection = mongo.db.todos
        todos_collection.insert_one({'_id': todo_id, 'task': task})
        return jsonify({'id': todo_id, 'task': task}), 201
    else:
        return jsonify({'error': 'Task is required'}), 400

@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    todo_data = request.json
    new_task = todo_data.get('task')
    if new_task:
        todos_collection = mongo.db.todos
        todos_collection.update_one({'_id': id}, {'$set': {'task': new_task}})
        return jsonify({'message': 'Todo updated successfully'}), 200
    else:
        return jsonify({'error': 'Task is required'}), 400

@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    todos_collection = mongo.db.todos
    todos_collection.delete_one({'_id': id})
    return jsonify({'message': 'Todo deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
