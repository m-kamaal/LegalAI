from fastapi import FastAPI, Path, Query, HTTPException
import json

file = "/Users/workpc/Legalai/FastAPI/sample_data.json"

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
    filter:str = Query(description="this decides if you want to filter by status of the task or priority"), 
    filter_value : str = Query(description= "values can be high, medium, low for priority and in_progress, pending, completed for status")
    ):
    





# if __name__ == "__main__":
#     resp =  get_data()
#     print(resp)
