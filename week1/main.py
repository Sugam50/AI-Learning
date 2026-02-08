from token import OP
from fastapi import FastAPI, Path, Query, Body, Header, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated, Optional
import uvicorn

app = FastAPI()
class Tasks(BaseModel):
    title: str
    description: str
    completed: bool

class updateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class AdditionalHeaders(BaseModel):
    x_token: Optional[str] = None
    x_key: Optional[str] = None
    authorisation: Optional[str] = None,

def get_additional_headers(
    x_token: Optional[str] = Header(default=None),
    x_key: Optional[str] = Header(default=None),
    authorisation: Optional[str] = Header(default=None),
) -> AdditionalHeaders:
    return AdditionalHeaders(
        x_token=x_token,
        x_key=x_key,
        authorisation=authorisation
    )

tasks = {
    1: Tasks(title="Task 1", description="Description 1", completed=False),
}

@app.get("/tasks/{task_id}")
def get_tasks(*, task_id: int = Path(..., description="The ID of the task"), name: str = None)->Tasks:
    if(name):
        for task in tasks:
            if tasks[task]['title'].lower() == name.lower():
                return tasks[task]
        return {"message": "Task not found"}
    return tasks[task_id]

@app.post("/tasks")
def create_task(*, taskId: int, task: Tasks = Body(...), AdditionalHeaders: Annotated[AdditionalHeaders,  Depends(get_additional_headers)]):
    print("headers", AdditionalHeaders.model_dump())
    if(taskId in tasks):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task already exists")
    tasks[taskId] = task
    return {"message": "Task created successfully", "task": task.model_dump()}  # to convert pydantic model to dictionary

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: updateTask):
    if(task_id not in tasks):
        return {"message": "Task not found"}

    if task.title:
        tasks[task_id].title = task.title
    if task.description:
        tasks[task_id].description = task.description
    if task.completed:
        tasks[task_id].completed = task.completed
    return {"message": "Task updated successfully", "task_id": task_id}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if(task_id not in tasks):
        return {"message": "Task not found"}
    del tasks[task_id]
    return {"message": "Task deleted successfully", "task_id": task_id}
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

