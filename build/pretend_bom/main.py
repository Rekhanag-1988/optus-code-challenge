import os
import requests
import json
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def pretend_bom():
    bom_data = json.load(open("static_bom.json"))
    return bom_data