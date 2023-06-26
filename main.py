from fastapi import FastAPI
from routes import user_router
from db import engine, create_all_tables
import uvicorn

app = FastAPI()


create_all_tables()

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
