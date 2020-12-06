from fastapi import APIRouter, Depends
from server.models.user import (
    TodoSchema,
    User
)
from server.routes.user import get_current_active_user
from server.database import (
    create_new_task_in_db,
    get_all_tasks_from_db,
    get_task_by_id_from_db,
    mark_task_in_db,
    delete_task_from_db
)

router = APIRouter()

@router.post("/new")
async def create_new_task(todo: TodoSchema, current_user: User = Depends(get_current_active_user)):
    todo_dict = todo.dict()
    result = await create_new_task_in_db(current_user.username, todo_dict)
    if not result:
        return {"message": "failed to add the taak"}
    return {"message": "task added successfully"}

@router.get("/all")
async def get_all_tasks(current_user: User = Depends(get_current_active_user)):
    result = await get_all_tasks_from_db(current_user.username)
    if not result:
        return {"tasks": "no tasks"}
    return {"tasks": result}

@router.get("/{task_id}")
async def get_task_by_id(task_id: str, current_user: User = Depends(get_current_active_user)):
    result = await get_task_by_id_from_db(current_user.username, task_id)
    if not result:
        return {"task": "no such task"}
    return result

@router.get("/mark/{task_id}")
async def mark_task(task_id: str, current_user: User = Depends(get_current_active_user)):
    result = await mark_task_in_db(current_user.username, task_id)
    return result

@router.delete("/{task_id}")
async def delete_task(task_id: str, current_user: User = Depends(get_current_active_user)):
    result = await delete_task_from_db(current_user.username, task_id)
    return result