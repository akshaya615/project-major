const alerts = [
  {
    id: 1,
    title: "High Risk Zone Detected",
    time: "5 mins ago",
    level: "High",
    location: "MG Road",
  },
  {
    id: 2,
    title: "Accident Prone Area 1 km Ahead",
    time: "10 mins ago",
    level: "Warning",
    location: "Jayanagar",
  },
  {
    id: 3,
    title: "Rainy Conditions – Drive Carefully",
    time: "30 mins ago",
    level: "Info",
    location: "Sarjapur Road",
  },
];

export default function Alerts() {
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