from fastapi import FastAPI
from server.routes.user import router as UserRouter
from server.routes.todo import router as TodoRouter

app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(TodoRouter, tags=["Todo"], prefix="/todo")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "User api accessible in /user"}