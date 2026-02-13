import axios from "axios";
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from "react-leaflet";
import { useEffect, useState } from "react";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import "leaflet.heat";

/* Fix marker icon */
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

/* 🔥 Heatmap Layer Component */
function HeatmapLayer({ points }) {
  const map = useMap();

  useEffect(() => {
    if (!map || points.length === 0) return;

    const heatLayer = L.heatLayer(points, {
      radius: 35,
      blur: 25,
      maxZoom: 15,
      gradient: {
        0.3: "#00ffcc",
        0.5: "#ffcc00",
        0.7: "#ff6600",
        1.0: "#ff0000",
      },
    }).addTo(map);

    return () => {
      map.removeLayer(heatLayer);
    };
  }, [map, points]);

  return null;
}

export default function LiveMap() {
  const [position, setPosition] = useState(null);
  const [route, setRoute] = useState([]);

  /* 🚦 Accident density points (Admin / ML generated) */
  const heatPoints = [
    [12.9716, 77.5946, 0.9],
    [12.972, 77.595, 0.7],
    [12.969, 77.592, 0.8],
    [12.925, 77.5938, 0.6],
  ];

  const [hotspots, setHotspots] = useState([]);

  useEffect(() => {
    axios
    .get("http://127.0.0.1:8000/hotspots")
    .then((res) => setHotspots(res.data))
    .catch((err) => console.error(err));
  }, []);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setPosition([pos.coords.latitude, pos.coords.longitude]);
      },
      () => alert("Location permission denied")
    );
  }, []);

  const drawRoute = async () => {
    const start = position;
    const end = [12.9352, 77.6245];

    const res = await fetch(
      `https://router.project-osrm.org/route/v1/driving/${start[1]},${start[0]};${end[1]},${end[0]}?overview=full&geometries=geojson`
    );
    const data = await res.json();
    setRoute(
      data.routes[0].geometry.coordinates.map((c) => [c[1], c[0]])
    );
  };

  if (!position) return <p>Loading map...</p>;

  return (
    <>
      <MapContainer center={position} zoom={13} style={{ height: "380px" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

        <HeatmapLayer points={heatPoints} />

        <Marker position={position}>
          <Popup>You are here</Popup>
        </Marker>

        {hotspots.map((h, i) => (
          <Marker key={i} position={[h.lat, h.lng]}>
            <Popup>
              🚦 <strong>{h.name}</strong> <br />
              Severity: {h.level}
            </Popup>
          </Marker>
        ))}

        {route.length > 0 && <Polyline positions={route} />}
      </MapContainer>

      <div className="route-info">
        <button onClick={drawRoute}>🧭 Start Navigation</button>
      </div>
    </>
  );
}