import FeedbackForm from "./FeedbackForm";

const LocationDetails = ({ location }) => {
  if (!location) return null;

  return (
    <div className="location-panel">
      <h3>{location.name}</h3>
      <p>Risk Level: {location.risk}</p>
      <p>Accidents Reported: {location.count}</p>

      <FeedbackForm locationId={location.id} />
    </div>
  );
};

export default LocationDetails;