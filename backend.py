import uvicorn
from fastapi import FastAPI

from config import HOST, PORT
from database.controllers.order import get_order
from servers.outline_keys import get_key


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
