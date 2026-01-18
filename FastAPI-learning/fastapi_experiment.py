from fastapi import FastAPI, Path, Query, HTTPException
import json
from typing import Literal

file = "/Users/workpc/Legalai/FastAPI-learning/sample_data.json"

def get_data():
    with open (file, "r") as f:
        return json.load(f)

app = FastAPI()



@app.get('/')
def homepage():
    return {'msg': 'WELCOME TO THE HOMEPAGE'}

@app.get('/view-all-tasks')
def view_all_data():
    values =  get_data()

    if values:
        return values
    raise HTTPException(status_code=400, detail="No Data found")


@app.get('/task/{task_id}')
def get_task(task_id: str = Path(..., pattern=r"^tsk_\d{4}$")):

    data = get_data()

    for task in data:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(status_code=404, detail="Task not found")

@app.get('/filtered-task')
def get_filtered_tasks(
    filter_name:Literal['status', 'priority'] = Query(description="this decides if you want to filter by status of the task or priority"), 
    filter_value : str = Query(description= "values can be high, medium, low for priority and in_progress, pending, completed for status")
    ):
    data = get_data()
    print(f"Filtering for {filter_name} == {filter_value}") # Debugging
    print(f"First item in data: {data[0] if data else 'Empty'}") # Debugging

    if filter_name == 'status':
        return [item for item in data if item.get(filter_name) == filter_value]
    if filter_name == 'priority':
        return [item for item in data if item.get(filter_name) == filter_value]

 


    

    


    


