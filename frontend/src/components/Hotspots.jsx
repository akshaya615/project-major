import L from "leaflet";
import { useEffect, useRef, useState } from "react";
import axios from "axios";
import "leaflet/dist/leaflet.css";

export default function Hotspots() {
  const mapRef = useRef(null);
  const [hotspots, setHotspots] = useState([]);

  // 🔥 Fetch hotspots from backend
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/hotspots/hdbscan")
      .then((res) => {
        // Backend returns:
        // { count: 4, hotspots: [...] }

        if (!res.data || !res.data.hotspots) return;

        const formattedHotspots = res.data.hotspots
          // Remove null coordinates
          .filter(
            (h) =>
              h.centroid_lat !== null &&
              h.centroid_lon !== null
          )
          // Remove duplicates
          .filter(
            (value, index, self) =>
              index ===
              self.findIndex(
                (t) =>
                  t.centroid_lat === value.centroid_lat &&
                  t.centroid_lon === value.centroid_lon
              )
          )
          // Convert to frontend format
          .map((h, index) => ({
            id: index + 1,
            name: `Cluster ${h.cluster_id}`,
            lat: h.centroid_lat,
            lng: h.centroid_lon,
            severity:
              h.density_score >= 0.8
                ? "High"
                : h.density_score >= 0.5
                ? "Medium"
                : "Low",
          }));

        setHotspots(formattedHotspots);
      })
      .catch((err) => console.error(err));
  }, []);

  // 🔥 Initialize Map
  useEffect(() => {
    if (!mapRef.current) return;

    const map = L.map(mapRef.current).setView(
      [12.9716, 77.5946],
      12
    );

    L.tileLayer(
      "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    ).addTo(map);

    // Add markers
    hotspots.forEach((h) => {
      L.marker([h.lat, h.lng])
        .addTo(map)
        .bindPopup(
          `<b>${h.name}</b><br/>Severity: ${h.severity}`
        );
    });

    return () => {
      map.remove();
    };
  }, [hotspots]);

  return (
    <div className="hotspot-wrapper">
      <h2>Accident Hotspots</h2>

      <div
        ref={mapRef}
        style={{ height: "300px", marginBottom: "15px" }}
      />

      <table className="hotspot-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Location</th>
            <th>Severity</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {hotspots.map((h, i) => (
            <tr key={h.id}>
              <td>{i + 1}</td>
              <td>{h.name}</td>
              <td>
                <span
                  className={`badge ${h.severity.toLowerCase()}`}
                >
                  {h.severity}
                </span>
              </td>
              <td>
                <button>View Location</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}