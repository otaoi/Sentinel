import redis
import json

#we need fastapi for speed and async, important for something like this
from fastapi import FastAPI, BackgroundTasks

#pydantic to help with being more statically typed
from pydantic import BaseModel

application =FastAPI()

#the decode responses should be true to return strings not byes
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

#we can defined what we want the sensor to return
class SensorData(BaseModel):
    id:str     #the id of the sensor could be sens-001
    lat:float  #latitude
    lon:float  #longitude
    temp:float #temp in celsious probably
    status:str #if its "ok" or "fire"

@application.post("/ingestion")
async def dataingestor(data: SensorData): #non blocking post with SensorData
    #sensor data is received here and then pushed into Redis Queue

    #convert to json
    package = data.json()

    #list push into fire_stream list fifo
    r.lpush("fire_stream",payload)

    #i dont wanna kill my ram so only keeping the first 2000 items
    r.ltrim("fire_stream", 0, 2000)

    #return a json to sensor
    return {"message": "data in queue", "status": "success"}

