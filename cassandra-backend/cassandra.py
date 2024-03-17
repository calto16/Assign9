
from flask import Flask, jsonify, request
from cassandra.cluster import Cluster
import uuid
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']

cluster = Cluster(app.config['CASSANDRA_HOSTS'])
session = cluster.connect()

# Create keyspace and table if not exists
keyspace_query = """
    CREATE KEYSPACE IF NOT EXISTS todo_keyspace
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
"""
session.execute(keyspace_query)

table_query = """
    CREATE TABLE IF NOT EXISTS todo_keyspace.todos (
        id UUID PRIMARY KEY,
        task text
    )
"""
session.set_keyspace('todo_keyspace')
session.execute(table_query)

@app.route('/todo', methods=['GET'])
def get_todo_list():
    query = "SELECT id, task FROM todos"
    rows = session.execute(query)
    todo_list = [{'id': row.id, 'task': row.task} for row in rows]
    return jsonify(todo_list)

@app.route('/todo', methods=['POST'])
def create_todo():
    todo_data = request.json
    task = todo_data.get('task')
    if task:
        todo_id = uuid.uuid4()
        query = "INSERT INTO todos (id, task) VALUES (%s, %s)"
        session.execute(query, (todo_id, task))
        return jsonify({'id': todo_id, 'task': task}), 201
    else:
        return jsonify({'error': 'Task is required'}), 400

@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    todo_data = request.json
    new_task = todo_data.get('task')
    if new_task:
        query = "UPDATE todos SET task = %s WHERE id = %s"
        session.execute(query, (new_task, uuid.UUID(id)))
        return jsonify({'message': 'Todo updated successfully'}), 200
    else:
        return jsonify({'error': 'Task is required'}), 400

@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    query = "DELETE FROM todos WHERE id = %s"
    session.execute(query, (uuid.UUID(id),))
    return jsonify({'message': 'Todo deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
