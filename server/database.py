import motor.motor_asyncio
from bson.objectid import ObjectId
from typing import Optional, Dict, List

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client.users_database
collection = db.users_collection

def user_helper(user) -> dict:
    return {
        "username": user["username"]
    }

## get user
async def get_user_from_db(username: str):
    user = await collection.find_one({"username": username})
    return user

## create new user
async def write_new_user_in_db(user: dict):
    Exist = await collection.find_one({"username": user["username"]})
    if not Exist:
        new_user = await collection.insert_one(user)
        saved_user = await collection.find_one({"_id": new_user.inserted_id})
        return user_helper(saved_user)
    return user_helper(Exist)

## create task
async def create_new_task_in_db(username: str, todo: dict):
    # todo["due_date"] = todo["due_date"].strftime("%x")
    todo.update({"_id": ObjectId()})
    user_db = await collection.find_one({"username": username})
    todos = user_db.get("tasks")
    todos.append(todo)
    result = await collection.update_one({"username": username}, { "$set": {"tasks": todos}})
    return result

## get all tasks
async def get_all_tasks_from_db(username: str):
    todos = await collection.find_one({"username": username})
    if not todos.get("tasks"):
        return False
    result = []
    for todo in todos["tasks"]:
        todo["_id"] = str(todo["_id"])
        result.append(todo)
    return result

## get task by id
async def get_task_by_id_from_db(username: str, task_id: str):
    user = await collection.find_one({"username": username})
    task = {}
    for u in user["tasks"]:
        if str(u["_id"]) == task_id:
            task = u
            task["_id"] = str(u["_id"])
            break
    if not task:
        return {"message": "task not found"}
    return task

## mark task as done
async def mark_task_in_db(username: str, task_id: str):
    user = await collection.find_one({"username": username})
    for task in user["tasks"]:
        if str(task["_id"]) == task_id:
            task["is_done"] = not task["is_done"]
            break
    result = await update_tasks(username, user["tasks"])
    if not result:
        return {"message": "failed to toggle task"}
    return {"message": "task toggled successully"}

## delete task by id
async def delete_task_from_db(username: str, task_id: str):
    user = await collection.find_one({"username": username})
    for i, task in enumerate(user["tasks"]):
        if str(task["_id"]) == task_id:
            del user["tasks"][i]
            break
    result = await update_tasks(username, user["tasks"])
    if not result:
        return {"message": "failed to delete task"}
    return {"message": "task deleted successfully"}


#### update tasks
async def update_tasks(username: str, tasks: List):
    result = await collection.update_one({"username": username}, { "$set": {"tasks": tasks}})
    return result