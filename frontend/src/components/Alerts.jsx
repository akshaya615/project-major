import { useEffect, useState } from "react";
import axios from "axios";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/alerts")
      .then((res) => setAlerts(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="alerts-wrapper">
      <h2>Alerts</h2>

      {alerts.map((a) => (
        <div key={a.id} className={`alert-card ${a.level.toLowerCase()}`}>
          <div>
            <strong>{a.title}</strong>
            <p>{a.time}</p>
          </div>
          <button>View Location</button>
        </div>
      ))}
    </div>
  );
}