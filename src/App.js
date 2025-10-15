// frontend/src/App.js

import React, { useRef, useEffect, useState, useCallback } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { FaTree } from 'react-icons/fa'; // Icon for our button

// --- Styles for our UI Overlay ---
const uiOverlayStyle = {
  position: 'absolute', top: '20px', left: '20px',
  backgroundColor: 'rgba(30, 30, 30, 0.8)', color: 'white',
  padding: '10px 15px', borderRadius: '8px', zIndex: 1,
  fontFamily: 'sans-serif', display: 'flex', flexDirection: 'column', gap: '10px'
};

const buttonStyle = {
  display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 15px',
  fontSize: '16px', border: 'none', borderRadius: '5px', color: 'white',
  cursor: 'pointer', transition: 'background-color 0.3s',
};

const App = () => {
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);

  // --- NEW: State Management ---
  const [interventions, setInterventions] = useState([]); // Stores locations of placed gardens
  const [isAddingMode, setIsAddingMode] = useState(false); // Are we in "add garden" mode?
  const [isLoading, setIsLoading] = useState(true); // Is a simulation running?

  // --- NEW: Function to Run Simulation ---
  const runSimulation = useCallback((currentInterventions) => {
    setIsLoading(true);
    fetch('http://127.0.0.1:5000/api/simulate', { // New endpoint
      method: 'POST', // New method
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ interventions: currentInterventions }),
    })
    .then(response => response.json())
    .then(data => {
      const map = mapRef.current;
      const geojsonData = {
        type: 'FeatureCollection',
        features: data.map(point => ({
          type: 'Feature', properties: { mag: point[2] },
          geometry: { type: 'Point', coordinates: [point[0], point[1]] },
        })),
      };
      const source = map.getSource('emissions-source');
      if (source) {
        source.setData(geojsonData); // Update existing data
      }
      setIsLoading(false);
    })
    .catch(error => {
      console.error("Error fetching simulation data:", error);
      setIsLoading(false);
    });
  }, []);

  // --- NEW: Map Click Handler ---
  const handleMapClick = useCallback((e) => {
    if (!isAddingMode) return;

    const newIntervention = { lat: e.lngLat.lat, lng: e.lngLat.lng };
    const updatedInterventions = [...interventions, newIntervention];
    
    setInterventions(updatedInterventions);
    setIsAddingMode(false);
    
    new maplibregl.Marker({ color: '#39FF14' }) // Neon green marker
      .setLngLat([newIntervention.lng, newIntervention.lat])
      .addTo(mapRef.current);
      
    runSimulation(updatedInterventions); // Re-run simulation
  }, [isAddingMode, interventions, runSimulation]);
  
  // --- Map Initialization ---
  useEffect(() => {
    const map = new maplibregl.Map({
      container: mapContainerRef.current,
      style: `https://api.maptiler.com/maps/streets-v2-dark/style.json?key=${process.env.REACT_APP_MAPTILER_KEY}`,
      center: [72.504, 23.241],
      zoom: 16, pitch: 65, bearing: -17.6,
    });
    mapRef.current = map;

    map.on('load', () => {
      map.addSource('emissions-source', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] }, // Start empty
      });
      map.addLayer({
        id: 'emissions-heatmap', type: 'heatmap', source: 'emissions-source',
        paint: {
          'heatmap-weight': ['interpolate', ['linear'], ['get', 'mag'], 0, 0, 1, 1],
          'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 11, 1, 18, 3],
          'heatmap-color': [
            'interpolate', ['linear'], ['heatmap-density'], 0, 'rgba(0, 255, 0, 0)',
            0.2, 'rgba(0, 255, 0, 0.5)', 0.5, 'rgba(255, 255, 0, 0.6)',
            0.8, 'rgba(255, 165, 0, 0.7)', 1, 'rgba(255, 0, 0, 0.8)'
          ],
          'heatmap-radius': ['interpolate', ['linear'], ['zoom'], 11, 15, 18, 40],
        }
      });
      runSimulation([]); // Run initial simulation
    });

    map.on('click', handleMapClick);

    return () => { map.off('click', handleMapClick); map.remove(); };
  }, [runSimulation, handleMapClick]);

  return (
    <div>
      <div style={uiOverlayStyle}>
        <h3>Controls</h3>
        <button 
          style={{...buttonStyle, backgroundColor: isAddingMode ? '#f44336' : '#4CAF50'}}
          onClick={() => setIsAddingMode(!isAddingMode)}
        >
          <FaTree /> {isAddingMode ? 'Cancel' : 'Add Vertical Garden'}
        </button>
        {isLoading && <p>Running Simulation...</p>}
      </div>
      <div ref={mapContainerRef} style={{ width: '100vw', height: '100vh' }} />
    </div>
  );
};

export default App;