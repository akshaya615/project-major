import { MapContainer, TileLayer, Marker, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet-routing-machine";
import "leaflet/dist/leaflet.css";
import { useEffect } from "react";

function Routing({ from, to, onRouteFound }) {
  const map = useMap();

  useEffect(() => {
    if (!from || !to) return;

    const routingControl = L.Routing.control({
      waypoints: [
        L.latLng(from.lat, from.lng),
        L.latLng(to.lat, to.lng)
      ],
      routeWhileDragging: false,
      show: false,
      addWaypoints: false,
      lineOptions: {
        styles: [{ color: "#ff3b3b", weight: 5 }]
      }
    })
      .on("routesfound", (e) => {
        const route = e.routes[0];
        onRouteFound({
          distance: (route.summary.totalDistance / 1000).toFixed(2),
          time: (route.summary.totalTime / 60).toFixed(1)
        });
      })
      .addTo(map);

    return () => map.removeControl(routingControl);
  }, [from, to]);

  return null;
}

export default function RouteMap({ from, to, onRouteFound }) {
  return (
    <MapContainer
      center={[12.9716, 77.5946]}
      zoom={13}
      style={{ height: "100vh", width: "100%" }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {from && <Marker position={[from.lat, from.lng]} />}
      {to && <Marker position={[to.lat, to.lng]} />}

      <Routing from={from} to={to} onRouteFound={onRouteFound} />
    </MapContainer>
  );
}