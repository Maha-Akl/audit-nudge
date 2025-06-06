from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

TASKS_FILE = 'tasks.json'

# Load tasks from file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = not task['done']
            break
    save_tasks(tasks)
    return render_template('partials/task_item.html', task=task)

@app.route('/progress')
def progress():
    tasks = load_tasks()
    total = len(tasks)
    completed = sum(1 for task in tasks if task['done'])
    percent = int((completed / total) * 100) if total else 0
    return render_template('partials/progress_bar.html', percent=percent)

@app.route('/add', methods=['POST'])
def add_task():
    tasks = load_tasks()
    label = request.form.get('label', '').strip()
    if label:
        new_id = max((task['id'] for task in tasks), default=0) + 1
        tasks.append({'id': new_id, 'label': label, 'done': False})
        save_tasks(tasks)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
