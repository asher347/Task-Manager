from flask import Flask, request, jsonify
from datetime import datetime
from flask import render_template
from flask_cors import CORS
import TaskManagerServer

app = Flask(__name__)
CORS(app)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    filter_criteria = request.args.get('filter')
    tasks = TaskManagerServer.get_tasks(filter_criteria)
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    name = data.get('name')
    due_date = datetime.strptime(data.get('due_date'), "%Y-%m-%d").date()  # המרה ל-`datetime.date`
    priority = data.get('priority')
    TaskManagerServer.create_task(name, due_date, priority)
    return jsonify({"message": "Task created"}), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    TaskManagerServer.update_task(task_id, data)
    return jsonify({"message": "Task updated"})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        TaskManagerServer.delete_task(task_id)
        return jsonify({"message": "Task deleted"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def mark_task_completed(task_id):
    TaskManagerServer.mark_task_completed(task_id)
    return jsonify({"message": "Task marked as completed"})

@app.route('/reminders', methods=['GET'])
def send_reminders():
    reminders = []
    for task_id in range(len(TaskManagerServer.tasks)):
        reminder = TaskManagerServer.send_reminder(task_id)
        if reminder:
            reminders.append(reminder)
    return jsonify(reminders)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
