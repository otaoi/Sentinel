#the simulator for the large scale IoT sensors

import uuid #this is for the sensors unique id
import random #for getting random coordinates and temps
import time #controls the request per second
import requests #to send data to gateway

#just initializing box of southernbc, fire prown

LATMIN, LATMAX = 49.0, 51.5
LONMIN, LONMAX = -122.0, -119.0

#hardcoding some coordinates of real historical disasters and some data
HISTORICALHOTSPOTS = [
    {"name": "Lytton (2021)",       "lat": 50.23, "lon": -121.58, "risk_mult": 0.8},
    {"name": "Kelowna (2003)",      "lat": 49.88, "lon": -119.49, "risk_mult": 0.6},
    {"name": "Shuswap (2023)",      "lat": 50.83, "lon": -119.20, "risk_mult": 0.7},
    {"name": "Manning Park (2022)", "lat": 49.06, "lon": -120.78, "risk_mult": 0.5},
                    ]

while True:
    #figure out if the sensor wakes up in a historical danger zone or new sector
    ishistorical = random.random() <0.40 #40%chance to be historical

    if ishistorical:
        spot = random.choice(HISTORICALHOTSPOTS)

        #since the sensorts are not all in one spot we randomize 5km cluster
        lat = spot["lat"] + random.uniform(-0.05, 0.05)
        lon = spot["lon"] + random.uniform(-0.05, 0.05)

        

