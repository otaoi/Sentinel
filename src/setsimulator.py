import time
import requests
import random
import sys

GATEWAY_URL = "http://localhost:8000/ingestion"
LYTTON_ID = "LYTTON-01"

#zone in history with fire
ZONES = [
    {"id": "KELOWNA-03", "lat": 49.88, "lon": -119.49},
    {"id": "SHUSWAP-23", "lat": 50.83, "lon": -119.20},
    {"id": "SAFE-01",    "lat": 49.00, "lon": -120.00},
]

current_state = "NORMAL"
incident_start = 0

while True:
    #random noise
    for zone in ZONES:
        requests.post(GATEWAY_URL, json={
            "id": zone["id"], "lat": zone["lat"], "lon": zone["lon"],
            "temp": random.uniform(22, 26), "status": "OK"
        })

    #controls the logic
    if current_state == "NORMAL":
        temp = 25.0 + random.uniform(-1, 1)
        status = "OK"
        sys.stdout.write(f"\rMONITORING HISTORICAL ZONES | Lytton: {temp:.1f}°C    ")
        sys.stdout.flush()

        # 10% Chance to trigger the "Theme Event"
        if random.random() < 0.10: 
            current_state = "INCIDENT"
            incident_start = time.time()
            print("\n\nANOMALY DETECTED IN LYTTON SECTOR (2021 ZONE)")

    elif current_state == "INCIDENT":
        elapsed = time.time() - incident_start
        
        if elapsed < 15: # YELLOW PHASE
            progress = elapsed / 15
            temp = 35.0 + (progress * 45.0) 
            status = "WARNING"
            print(f"[T+{elapsed:.0f}s] PRE-IGNITION SPIKE: {temp:.1f}°C (MATCHING 2021 PATTERN)")

        elif 15 <= elapsed < 25: # RED PHASE
            temp = 450.0 + random.uniform(-10, 50)
            status = "FIRE"
            print(f"[T+{elapsed:.0f}s] IGNITION CONFIRMED: {temp:.0f}°C")
            
        elif 25 <= elapsed < 30: # COOL DOWN
            temp = 100.0 - ((elapsed-25) * 10)
            status = "WARNING"
            print(f"[T+{elapsed:.0f}s] THREAT SUPPRESSED. Temp dropping.")
            
        else:
            print("\n HISTORICAL SECTOR SECURED. RESUMING PATROL.\n")
            current_state = "NORMAL"

    #try to send data
    try:
        requests.post(GATEWAY_URL, json={
            "id": LYTTON_ID, "lat": 50.23, "lon": -121.58,
            "temp": temp, "status": status
        }, timeout=0.1)
    except: pass
    time.sleep(1.0)