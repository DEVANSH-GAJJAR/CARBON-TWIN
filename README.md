# 🌬️🏙️ UrbanCarbonTwin

A dynamic 3D digital twin for simulating CO₂ dispersion and the impact of carbon capture interventions in urban environments.  
Developed for the **Smart India Hackathon 2025**.

---

## ✨ Features

- **3D Digital Twin**: Renders a realistic, interactive 3D model of *Kalol, Gujarat*.
- **Dynamic Simulation**: Simulates CO₂ dispersion using a Gaussian plume model and real-time wind data.
- **"What-If" Analysis**: Place virtual carbon capture interventions (e.g., vertical gardens) and see the immediate impact on CO₂ hotspots.
- **IoT Integration**: Includes a simulator for IoT sensors sending live air quality data to a cloud dashboard (ThingsBoard).

---

## 🛠️ Tech Stack

| Category | Technology |
|-----------|-------------|
| **Frontend** | React.js, MapLibre GL JS |
| **Backend** | Python, Flask, OSMnx, NumPy |
| **IoT & Messaging** | ThingsBoard, Paho-MQTT |
| **APIs & Services** | OpenWeatherMap, MapTiler |

---

## 🚀 Getting Started

Follow these steps to set up the project locally.

### Prerequisites

- Python 3.8+
- Node.js & npm
- Git

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/DEVANSH-GAJJAR/CARBON-TWIN.git
cd CARBON-TWIN

```
### 2️⃣ Setup the backend 

```bash

# Go to the backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install Flask Flask-Cors osmnx requests numpy paho-mqtt shapely

# Download local map data (one-time step)
python download_map.py
```
