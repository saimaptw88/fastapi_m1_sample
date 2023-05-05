from fastapi import FastAPI

app = FastAPI()
app.include_router(task.router)
app.include_router(done.router)


@app.get("/hello")
async def hello():
    return {"message": "hello world"}
