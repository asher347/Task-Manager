from datetime import datetime
import requests


def get_date_from_user(prompt="Enter a due date (YYYY-MM-DD): "):
    while True:
        user_input = input(prompt)
        try:
            date = datetime.strptime(user_input, "%Y-%m-%d")
            return date
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")

def addtask():
    name = input("Enter name for task: ")
    due_date = get_date_from_user()
    priority = input("Enter priority (Low/Medium/High):")

    response = requests.post('http://127.0.0.1:5000/tasks', json={
        'name': name,
        'due_date': due_date.strftime('%Y-%m-%d'),
        'priority': priority
    })
    
    if response.status_code == 201:
        print("Task added successfully")
    else:
        print("Failed to add task:", response.json())


def displayTasks(filter=None):
    params = {'filter': filter} if filter else {}
    response = requests.get('http://127.0.0.1:5000/tasks', params=params)
    
    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            print(task)
    else:
        print("Failed to retrieve tasks:", response.json())


def editTask(task_id):
    print("Enter new details for the task:")
    name = input("Enter new name for task (leave blank to keep current): ")
    due_date = input("Enter new due date (YYYY-MM-DD) (leave blank to keep current): ")
    priority = input("Enter new priority (Low/High) (leave blank to keep current): ")
    
    new_values = {}
    if name:
        new_values['name'] = name
    if due_date:
        new_values['due_date'] = datetime.strptime(due_date, "%Y-%m-%d").date().strftime('%Y-%m-%d')
    if priority:
        new_values['priority'] = priority
    
    response = requests.put(f'http://127.0.0.1:5000/tasks/{task_id}', json=new_values)
    
    if response.status_code == 200:
        print("Task updated successfully")
    else:
        print("Failed to update task:", response.json())

def removeTask(task_id):
    response = requests.delete(f'http://127.0.0.1:5000/tasks/{task_id}')
    
    if response.status_code == 200:
        print("Task deleted successfully")
    else:
        print("Failed to delete task:", response.json())


def completeTask(task_id):
    response = requests.put(f'http://127.0.0.1:5000/tasks/{task_id}/complete')
    
    if response.status_code == 200:
        print("Task marked as completed")
    else:
        print("Failed to mark task as completed:", response.json())

def filterTasks(filter_criteria=None):

    if filter_criteria is None:
        filter_criteria = input("Enter the filter (name, due_date, priority): ").lower()
    
    categories = ['name', 'due_date', 'priority']
    
   
    if filter_criteria not in categories:
        raise ValueError("Invalid filter criteria.")
    
    response = requests.get(f'http://127.0.0.1:5000/tasks', params={'filter': filter_criteria})
    
    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            print(task)
    else:
        print("Failed to retrieve tasks:", response.json())


