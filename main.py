from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    delete_todo
)
from model import Todo

app = FastAPI()
origins = ['https://localchost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo{title}", response_model=Todo)
async def get_todo_by_title(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(status_code=404, detail=f"Todo not found for this {title}")

@app.post("/api/todo", response_model=Todo)
async def post_todo(todo:Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(status_code=400, detail=f"Something went wrong")

@app.put("/api/todo{title}", response_model=Todo)
async def put_todo(title: str, description: str):
    response = await update_todo(title, description)
    if response:
        return response
    raise HTTPException(status_code=404, detail=f"Todo not found for this {title}")

@app.delete("/api/todo{title}")
async def delete_todo(title: str):
    response = await delete_todo(title)
    if response:
        return response
    raise HTTPException(status_code=404, detail=f"Todo not found for this {title}")

