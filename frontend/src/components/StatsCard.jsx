const StatsCard = ({ title, value }) => {
  return (
    <div style={{
      background: "rgba(255,255,255,0.1)",
      padding: "15px",
      borderRadius: "8px",
      minWidth: "160px"
    }}>
      <h4>{title}</h4>
      <h2>{value}</h2>
    </div>
  );
};

export default StatsCard;