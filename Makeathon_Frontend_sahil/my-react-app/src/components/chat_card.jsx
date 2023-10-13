import React from 'react';
import '../css/chat_card.css'; // Import the CSS file for styling

function RedBusCard({ title, description, imageSrc, buttonText }) {
  const cardStyle = {
    background: `url(${imageSrc})`,
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'right',
  };

  // Function to handle the button click and redirect
  const handleButtonClick = () => {
    // Use window.location to redirect to the desired URL
    window.location.href = 'http://127.0.0.1:3001/';
  };

  return (
    <div className="redbus-card" style={cardStyle}>
      <div className="redbus-card-content">
        <div className="logo-container">
          <img src="buddy-on-go.png" alt="Logo" className="logo" />
        </div>
        <h3 className="redbus-card-title">{title}</h3>
        <p className="redbus-card-description">{description}</p>
        <button className="chat-now-button" onClick={handleButtonClick}>
          {buttonText}
        </button>
      </div>
    </div>
  );
}

export default RedBusCard;
