import React from 'react';
import '../css/chat_card.css'; // Import the CSS file for styling

function RedBusCard({ title, description, imageSrc, buttonText }) {
  const cardStyle = {
    background: `url(${imageSrc})`,
   
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'right',
    
    
  };

  return (
    <div className="redbus-card" style={cardStyle}>
      <div className="redbus-card-content">
        <div className="logo-container">
          <img src="buddy-on-go.png" alt="Logo" className="logo" />
        </div>
        
        <h3 className="redbus-card-title">{title}</h3>
        <p className="redbus-card-description">{description}</p>
        <button className="chat-now-button">{buttonText}</button>
      </div>
    </div>
  );
}

export default RedBusCard;
