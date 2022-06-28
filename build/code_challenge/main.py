import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import List

app = FastAPI()

class errorResponseModel(BaseModel):
    error: str

class dataResponseModel(BaseModel):
    name: str
    apparent_t: float
    lat: float
    lon: float

def get_bom_session():
    """ returns request object """
    bom_session = requests.Session()
    bom_session.headers.update(
        {
            "Content-type": "application/json",
            "Accept": "application/json"
        }
    )
    return bom_session

@app.get("/",
    responses={
        503: {"model": errorResponseModel},
        404: {"model": errorResponseModel},
        500: {"model": errorResponseModel},
    },
    response_model=List[dataResponseModel]
)
async def code_challenge():      
    bom_session = get_bom_session()
    filtered_data = []
    try:
        response = bom_session.get("https://pretend-bom-7moui6f4lq-km.a.run.app/")
        response.raise_for_status()
        whether_data = response.json()
    except requests.ConnectionError as conn_err:
        return JSONResponse(status_code=503, content={"error": "Error connecting to BOM"})
    except requests.HTTPError as http_err:
        return JSONResponse(status_code=404, content={"error": "Requested resource is not found"})
    except Exception as unknown_err:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error."})
    
    for station  in whether_data["observations"]["data"]:
        if station["apparent_t"] > 10:
            station_data = {
                "name": station["name"],
                "apparent_t": station["apparent_t"],
                "lat": station["lat"],
                "lon": station["lon"] 
            }
            filtered_data.append(station_data)
        
    filtered_data = sorted(filtered_data, key=lambda d: d["apparent_t"]) 
    return filtered_data