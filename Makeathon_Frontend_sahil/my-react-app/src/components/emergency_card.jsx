import React from 'react';
import '../css/emergency_card.css'; // Import the CSS file for styling

function EmergencyCard({ title, description, imageSrc, buttonText }) {
  return (
    <div className="emergency-card">
      <div className="emergency-card-content">
        <h3 className="emergency-card-title">{title}</h3>
        <p className="emergency-card-description">{description}</p>
        <button className="emergency-card-button">{buttonText}</button>
      </div>
    </div>
  );
}

export default EmergencyCard;
