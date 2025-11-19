from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List



class prueba(BaseModel):
    respuesta : str


app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
     CORSMiddleware,
     allow_origins = "*",
     allow_credentials = True,
     allow_methods = ["*"],
     allow_headers =  ["*"]
)


memory_db = {"respuesta": "hola we"}

@app.get("/hola")
def si_la_mami():
    return{"hola" : "we"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


