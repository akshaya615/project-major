import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import Feedback from "../components/Feedback";
import VoiceAlert from "../components/VoiceAlert";

/* ✅ ADD THIS */
import Alerts from "../components/Alerts";
import Hotspots from "../components/Hotspots";

import "../styles/userDashboard.css";

export default function UserDashboard() {
  /* ================= UI STATE ================= */
  const [tab, setTab] = useState("home");
  const [open, setOpen] = useState(false);
  const [theme, setTheme] = useState("default");

  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");

  const dropdownRef = useRef(null);
  const navigate = useNavigate();

  /* ================= MAP STATE ================= */
  const mapRef = useRef(null);
  const map = useRef(null);
  const userMarker = useRef(null);
  const routeLayer = useRef(null);

  const [currentPos, setCurrentPos] = useState(null);
  const [routeCoords, setRouteCoords] = useState([]);

  /* ================= THEME / LOGOUT ================= */
  const toggleTheme = () =>
    setTheme((p) => (p === "default" ? "light" : "default"));
  const handleLogout = () => navigate("/login");

  /* ================= DROPDOWN ================= */
  useEffect(() => {
    const close = (e) =>
      dropdownRef.current &&
      !dropdownRef.current.contains(e.target) &&
      setOpen(false);

    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, []);

  /* ================= MAP INIT ================= */
  useEffect(() => {
    if (map.current) return;

    map.current = L.map(mapRef.current).setView(
      [20.5937, 78.9629],
      5
    );

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap",
    }).addTo(map.current);

    navigator.geolocation.watchPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;

        setCurrentPos([lat, lng]);

        document.getElementById("lat").innerText = lat.toFixed(6);
        document.getElementById("lng").innerText = lng.toFixed(6);

        if (!userMarker.current) {
          userMarker.current = L.marker([lat, lng]).addTo(map.current);
        } else {
          userMarker.current.setLatLng([lat, lng]);
        }
      },
      () => alert("Location permission denied"),
      { enableHighAccuracy: true }
    );
  }, []);

  /* ================= NAVIGATION ================= */
  const startNavigation = async () => {
    if (!to.trim()) return alert("Enter destination");

    let fromLat, fromLng;

    if (from.trim()) {
      const res = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${from}`
      );
      const data = await res.json();
      if (!data.length) return alert("From location not found");
      fromLat = +data[0].lat;
      fromLng = +data[0].lon;
    } else {
      if (!currentPos) return alert("Current location not ready");
      [fromLat, fromLng] = currentPos;
    }

    const toRes = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${to}`
    );
    const toData = await toRes.json();
    if (!toData.length) return alert("Destination not found");

    const toLat = +toData[0].lat;
    const toLng = +toData[0].lon;

    const routeRes = await fetch(
      `https://router.project-osrm.org/route/v1/driving/${fromLng},${fromLat};${toLng},${toLat}?overview=full&geometries=geojson`
    );
    const routeData = await routeRes.json();

    const coords = routeData.routes[0].geometry.coordinates.map(
      ([lng, lat]) => [lat, lng]
    );

    setRouteCoords(coords);

    if (routeLayer.current)
      map.current.removeLayer(routeLayer.current);

    routeLayer.current = L.polyline(coords, {
      color: "blue",
      weight: 5,
    }).addTo(map.current);

    map.current.fitBounds(routeLayer.current.getBounds());
  };

  /* ================= HOTSPOTS MARKERS (KEEP AS IS) ================= */
  useEffect(() => {
    if (tab !== "hotspots" || !map.current) return;

    const hotspots = [
      [12.9716, 77.5946],
      [17.385, 78.4867],
      [19.076, 72.8777],
    ];

    const markers = hotspots.map((p) =>
      L.circleMarker(p, {
        radius: 8,
        color: "red",
        fillOpacity: 0.7,
      })
        .bindPopup("⚠ Accident Prone Area")
        .addTo(map.current)
    );

    return () => markers.forEach((m) => map.current.removeLayer(m));
  }, [tab]);

  /* ================= UI ================= */
  return (
    <div className={`user-wrapper ${theme}`}>
      {/* NAVBAR */}
      <div className="user-navbar">
        <div className="nav-left">
          <span onClick={() => setTab("home")}>🏠 Home</span>
          <span onClick={() => setTab("alerts")}>Alerts</span>
          <span onClick={() => setTab("hotspots")}>Hotspots</span>
          <span onClick={() => setTab("feedback")}>Feedback</span>
        </div>

        <div className="profile-area" ref={dropdownRef}>
          <span onClick={() => setOpen(!open)}>Welcome, John ⬇</span>
          {open && (
            <div className="profile-dropdown">
              <div onClick={toggleTheme}>🌗 Switch Theme</div>
              <div className="danger" onClick={handleLogout}>
                🚪 Logout
              </div>
            </div>
          )}
        </div>
      </div>

      {/* CONTENT */}
      <div className="content">
        {tab === "home" && (
          <>
            <div className="location-card">
              <strong>Lat:</strong> <span id="lat">--</span> |{" "}
              <strong>Lon:</strong> <span id="lng">--</span>
            </div>

            <div className="home-grid">
              <div className="plan-card">
                <label>From</label>
                <input
                  value={from}
                  onChange={(e) => setFrom(e.target.value)}
                />

                <label>To</label>
                <input
                  value={to}
                  onChange={(e) => setTo(e.target.value)}
                />

                <button onClick={startNavigation}>
                  Start Navigation
                </button>
              </div>

              <div className="map-card">
                <div ref={mapRef} style={{ height: "100%" }} />
              </div>
            </div>
          </>
        )}

        {/* ✅ ALERTS — ADDED, NOTHING REMOVED */}
        {tab === "alerts" && (
          <>
            <Alerts />
            <VoiceAlert route={routeCoords} currentPos={currentPos} />
          </>
        )}

        {/* ✅ HOTSPOTS UI — MAP ALREADY ACTIVE */}
        {tab === "hotspots" && (
          <>
            <Hotspots />
            <div className="map-card">
              <div ref={mapRef} style={{ height: "100%" }} />
            </div>
          </>
        )}

        {tab === "feedback" && <Feedback />}
      </div>
    </div>
  );
}