import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

export default function MapView() {
  const mapRef = useRef(null);
  const markerRef = useRef(null);
  const routeRef = useRef(null);

  const destinationRef = useRef(null);
  const stepsRef = useRef([]);
  const stepIndexRef = useRef(0);

  // ===============================
  // MAP INIT
  // ===============================
  useEffect(() => {
    if (mapRef.current) return;

    mapRef.current = L.map("map").setView([20.5937, 78.9629], 5);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap",
    }).addTo(mapRef.current);

    const carIcon = L.icon({
      iconUrl: "https://cdn-icons-png.flaticon.com/512/744/744465.png",
      iconSize: [36, 36],
      iconAnchor: [18, 18],
    });

    // ===============================
    // LIVE GPS (marker only)
    // ===============================
    navigator.geolocation.watchPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;

        // Update dashboard numbers
        const latEl = document.getElementById("lat");
        const lngEl = document.getElementById("lng");
        if (latEl) latEl.innerText = lat.toFixed(6);
        if (lngEl) lngEl.innerText = lng.toFixed(6);

        if (!markerRef.current) {
          markerRef.current = L.marker([lat, lng], { icon: carIcon }).addTo(
            mapRef.current
          );
        } else {
          markerRef.current.setLatLng([lat, lng]);
        }

        checkNextTurn(lat, lng);
      },
      () => alert("Location permission denied"),
      { enableHighAccuracy: true }
    );
  }, []);

  // ===============================
  // GLOBAL NAVIGATION FUNCTION
  // ===============================
  window.startNavigation = async (fromText, toText) => {
    try {
      const from = fromText
        ? await geocode(fromText)
        : await getCurrentLocation();

      const to = await geocode(toText);

      destinationRef.current = to;
      stepIndexRef.current = 0;

      drawRoute(from, to);
      mapRef.current.setView([from.lat, from.lng], 14);
    } catch (e) {
      alert("Location not found");
    }
  };

  // ===============================
  // ROUTE DRAWING
  // ===============================
  async function drawRoute(from, to) {
    const url = `https://router.project-osrm.org/route/v1/driving/${from.lng},${from.lat};${to.lng},${to.lat}?overview=full&geometries=geojson&steps=true`;

    const res = await fetch(url);
    const data = await res.json();
    const route = data.routes[0];

    if (routeRef.current) {
      mapRef.current.removeLayer(routeRef.current);
    }

    routeRef.current = L.geoJSON(route.geometry, {
      style: { color: "#1a73e8", weight: 6 },
    }).addTo(mapRef.current);

    stepsRef.current = route.legs[0].steps;
    speak(stepsRef.current[0].maneuver.instruction);
  }

  // ===============================
  // TURN CHECKING
  // ===============================
  function checkNextTurn(lat, lng) {
    const step = stepsRef.current[stepIndexRef.current];
    if (!step) return;

    const [slng, slat] = step.maneuver.location;
    const d = distance(lat, lng, slat, slng);

    if (d < 30) {
      stepIndexRef.current++;
      if (stepsRef.current[stepIndexRef.current]) {
        speak(stepsRef.current[stepIndexRef.current].maneuver.instruction);
      } else {
        speak("You have arrived at your destination");
        destinationRef.current = null;
      }
    }
  }

  // ===============================
  // HELPERS
  // ===============================
  function speak(text) {
    speechSynthesis.cancel();
    speechSynthesis.speak(new SpeechSynthesisUtterance(text));
  }

  async function geocode(place) {
    const res = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
        place
      )}`
    );
    const data = await res.json();
    if (!data.length) throw new Error("Not found");
    return { lat: +data[0].lat, lng: +data[0].lon };
  }

  async function getCurrentLocation() {
    return new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        (p) =>
          resolve({
            lat: p.coords.latitude,
            lng: p.coords.longitude,
          }),
        reject
      );
    });
  }

  function distance(lat1, lon1, lat2, lon2) {
    const R = 6371e3;
    const φ1 = (lat1 * Math.PI) / 180;
    const φ2 = (lat2 * Math.PI) / 180;
    const Δφ = ((lat2 - lat1) * Math.PI) / 180;
    const Δλ = ((lon2 - lon1) * Math.PI) / 180;
    const a =
      Math.sin(Δφ / 2) ** 2 +
      Math.cos(φ1) *
        Math.cos(φ2) *
        Math.sin(Δλ / 2) ** 2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  }

  return <div id="map" style={{ height: "100vh" }} />;
}