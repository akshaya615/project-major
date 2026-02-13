import { MapContainer, TileLayer } from "react-leaflet";
import { useNavigate } from "react-router-dom";
import "leaflet/dist/leaflet.css";
import "./Landing.css";

function Landing() {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <MapContainer
        center={[17.385044, 78.486671]}
        zoom={11}
        className="map"
        whenCreated={(map) => {
          setTimeout(() => {
            map.invalidateSize();
          }, 200);
        }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
      </MapContainer>

      <div className="overlay">
        <h1>Accident Prediction System</h1>
        <p>Predicting accidents today to protect lives tomorrow.</p>

        <button
          className="login-btn"
          onClick={() => navigate("/login")}
        >
          Login
        </button>
      </div>
    </div>
  );
}

export default Landing;
