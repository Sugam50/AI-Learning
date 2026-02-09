from token import OP
from fastapi import BackgroundTasks, FastAPI, Path, Query, Body, Header, Response, status, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Annotated, Optional
from fastapi.routing import APIRouter
import uvicorn
import time
import asyncio
from fastapi.responses import StreamingResponse

import logging
import json
from uuid import uuid4

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

app = FastAPI()
class Tasks(BaseModel):
    title: str
    description: str
    completed: bool = False

class updateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class AdditionalHeaders(BaseModel):
    x_token: Optional[str] = None
    x_key: Optional[str] = None
    authorization: Optional[str] = None,

def get_additional_headers(
    x_token: Optional[str] = Header(default=None),
    x_key: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
) -> AdditionalHeaders:
    return AdditionalHeaders(
        x_token=x_token,
        x_key=x_key,
        authorization=authorization
    )

def router_auth_middleware(request: Request, AdditionalHeaders: Annotated[AdditionalHeaders,  Depends(get_additional_headers)]):
    auth = request.headers.get("Authorization")
    print("AdditionalHeaders", AdditionalHeaders.model_dump())
    if(auth != 'hello'):
        raise HTTPException(status_code=401, detail="INVALID AUTH")
    return request

tasks = {
    1: Tasks(title="Task 1", description="Description 1", completed=False),
}

router = APIRouter(dependencies=[Depends(router_auth_middleware)])

def slow_task(task_id: int):
    time.sleep(10)
    print(f"Task {task_id} processed")

async def stream_text(task_id: int):
    for i in range(10):
        yield f"Line {i}\n"
        await asyncio.sleep(1)
    print(f"Task {task_id} streamed")


@app.middleware("http")
async def log_requests(request, call_next):
    request_id = str(uuid4())
    logging.info(json.dumps({
        "request_id": request_id,
        "method": request.method,   
        "path": request.url.path,
    }))
    response = await call_next(request)
    return response

@router.get("/tasks/{task_id}")
def get_tasks(*, task_id: int = Path(..., description="The ID of the task"), name: str = None)->Tasks:
    if(name):
        for task in tasks:
            if tasks[task]['title'].lower() == name.lower():
                return tasks[task]
        return {"message": "Task not found"}
    return tasks[task_id]

@router.post("/tasks")
def create_task(*, taskId: int, task: Tasks = Body(...)):
    print("headers", AdditionalHeaders.model_dump())
    if(taskId in tasks):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task already exists")
    tasks[taskId] = task
    return {"message": "Task created successfully", "task": task.model_dump()}  # to convert pydantic model to dictionary

@router.put("/tasks/{task_id}")
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

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if(task_id not in tasks):
        return {"message": "Task not found"}
    del tasks[task_id]
    return {"message": "Task deleted successfully", "task_id": task_id}

@router.post("/tasks/{task_id}/process")
async def process_task(task_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(slow_task, task_id)
    return {"message": "Processing started", "task_id": task_id}    

@router.get("/tasks/{task_id}/stream")
async def get_stream(task_id: int):
    return StreamingResponse(stream_text(task_id), media_type="text/plain")



app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

