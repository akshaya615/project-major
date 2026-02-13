import { useState } from "react";

export default function Feedback() {
  const [message, setMessage] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = () => {
    if (!message.trim()) return;
    setSubmitted(true);
  };

  return (
    <div className="feedback-wrapper">
      <div className="feedback-card">
        {!submitted ? (
          <>
            <h3>We value your feedback</h3>
            <p>Help us improve road safety and navigation</p>

            <textarea
              placeholder="Share your experience..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />

            <button onClick={handleSubmit}>
              Submit Feedback
            </button>
          </>
        ) : (
          <div className="feedback-success">
            <h3>Thank you for your feedback</h3>
            <p>
              We have received your feedback and will review it carefully.
              <br />
              Your input helps us improve the system.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}