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

### 3️⃣ Setup the Frontend 

```bash
# Go to the frontend directory
cd frontend

# Install dependencies
npm install

```
Create a  .env  in frontend and add: 
```bash
REACT_APP_MAPTILER_KEY=YOUR_MAPTILER_API_KEY
```
---

### 🏃‍♂️ Usage

You’ll need two separate terminals.

Terminal 1 – Run the Backend Server

```bash 
# From /backend
.\venv\Scripts\activate
python app.py

```

Terminal 2 – Run the Frontend App

```bash

# From /frontend
npm start

```

this runs at localhost:3000

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/Frontend-React.js-61DAFB.svg)](https://react.dev/)
[![Flask](https://img.shields.io/badge/Backend-Flask-000000.svg)](https://flask.palletsprojects.com/)
[![MapLibre](https://img.shields.io/badge/Map-MapLibre%20GL%20JS-3CB371.svg)](https://maplibre.org/)
[![OpenWeatherMap](https://img.shields.io/badge/API-OpenWeatherMap-orange.svg)](https://openweathermap.org/)
