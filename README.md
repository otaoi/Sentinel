# Sentinel
## Predictive Wildfire Defense Grid

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-green)
![Redis](https://img.shields.io/badge/Redis-In--Memory-red)
![Status](https://img.shields.io/badge/System-Operational-brightgreen)

---

## Problem
In 2021, the town of Lytton, BC was destroyed by wildfire in under 20 minutes. Current detection methods rely heavily on satellite imagery, which has significant drawbacks:
* **High Latency:** Satellites only pass over BC every 6-12 hours.
* **Line of Sight:** Cameras require visibility and are often blocked by smoke rising.
* **Reactive:** Detection mostly occurs after the fire has grown significantly.

## Solution
Sentinel is a network of sensors placed directly on the forest floor. Instead of waiting for satellites to spot smoke, Sentinel detects sudden temperature spikes in the soil. This could provide a 48-hour warning before a fire actually ignites, allowing crews to stop the threat early.

---

## Architecture: Systems for Scale
The architecture prioritizes write-throughput and fault tolerance. The system handles 100,000+ sensor writes per second via a non-blocking pipeline.

### 1. Ingestion Layer (FastAPI)
* **Function:** High-concurrency gateway accepting raw JSON packets.
* **Performance:** Uses asynchronous non-blocking I/O.
* **Configuration:** Logging disabled in production to maximize throughput.

### 2. Buffer Layer (Redis Streams)
* **Function:** Decouples ingestion from the visualization/analysis layer.
* **Benefit:** Prevents backpressure on the ingestion server during the visualization rendering. Data is buffered in RAM for super fast access.

### 3. Command Layer (Rich CLI)
* **Function:** Low-latency Mission Control interface.
* **Design:** A Terminal User Interface (TUI) was selected over a web dashboard to ensure functionality in low-bandwidth environments and on low-power hardware typical of base camps.

---

## Theme Integration
The system integrates historical wildfire data to weight risk probabilities.

* **Historical Tracking:** GPS coordinates for the Lytton (2021) and Kelowna (2003) fires.
* **Weighted Logic:** Sensitivity multiplier is applied to sensors within these historical zones.
* **Outcome:** Thermal anomalies in scar zones escalate to "Pre-Ignition Events" faster than random sectors, utilizing past data points to enhance future protection.

---

## Quick Start

Three separate terminal windows are required to simulate the distributed system components. It is recommended that you create a virtual environment first.

### Prerequisites
```bash
pip install fastapi uvicorn redis rich requests pydantic
#make sure redis is running locally
```

### How to run
```bash
#run each command on a different window in linux
uvicorn gateway:application
python setsimulator.py
python monitor2.py
