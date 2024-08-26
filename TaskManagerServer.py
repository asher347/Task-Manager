
from datetime import datetime
tasks = []

def create_task(task_name, due_date, priority):
    global tasks
    task = {
        'name': task_name,
        'due_date': due_date,
        'priority': priority,
        'task_completed': "No"

    }
    tasks.append(task)



def get_tasks(filter=None):
    global tasks
    if filter:
        filtered_tasks = sorted(tasks, key=lambda x: x.get(filter, ''))
    else:
        filtered_tasks = tasks

    # המרת התאריכים לאורח JSON
    for task in filtered_tasks:
        if isinstance(task['due_date'], datetime):
            task['due_date'] = task['due_date'].isoformat()
        else:
            # אם התאריך כבר ב-ISO format (string), לא צריך להמיר
            pass

    return filtered_tasks
def update_task(task_id, new_values):
    global tasks
    task = tasks[task_id]
    task.update(new_values)

def delete_task(task_id):
    global tasks
    try:
        del tasks[task_id]
    except IndexError:
        raise ValueError("No task with this ID")

def mark_task_completed(task_id):
    global tasks
    tasks[task_id]["task_completed"]="Yes"

def send_reminder(task_id):
    global tasks
    current_date = datetime.now().date()
    task = tasks[task_id]
    if task['due_date'] == current_date:
        return f"Reminder: {task}"
    return None



