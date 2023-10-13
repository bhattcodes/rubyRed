import React from 'react';
import WeatherCard from './weather_card'; // Import your WeatherCard component
import '../css/weatherwidget.css'; // Import the CSS for the widget styling

function WeatherWidget() {
  return (
    <div className="weather-widget">
      <WeatherCard title="Today's Weather" buttonText="Details" />
    </div>
  );
}

export default WeatherWidget;
