import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../css/weather_card.css'; // Import the CSS file for styling

function WeatherCard({ title, buttonText }) {
  const [description, setDescription] = useState('');
  const [temperature, setTemperature] = useState('');
  const [weatherCondition, setWeatherCondition] = useState('');

  useEffect(() => {
    // Function to fetch weather data from your API
    const fetchWeatherData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/get_weather?lat=12.958184&lon=77.6421466');
        console.log(response);

        if (response.status === 200) {
          const weatherData = response.data;

          // Convert temperature from Kelvin to Celsius
          const celsiusTemperature = (weatherData.Temperature - 273.15).toFixed(2);

          // Extract temperature and weather description and set the component state
          setTemperature(`Temperature: ${celsiusTemperature}°C`);
          setDescription(` ${weatherData['Weather Description']}`);
          setWeatherCondition(weatherData['Weather Description']);
        } else {
          setDescription('Error: Unable to retrieve weather information');
        }
      } catch (error) {
        console.error(error);
        setDescription('Error: Unable to retrieve weather information');
      }
    };

    // Fetch weather data when the component mounts
    fetchWeatherData();
  }, []);

  // Function to map weather descriptions to corresponding GIFs
  const getWeatherGif = (weatherCondition) => {
    // Convert the weather condition to lowercase for a case-insensitive check
    const lowercaseCondition = weatherCondition.toLowerCase();
  
    if (lowercaseCondition.includes('rain')) {
      return 'rainy.gif'; // Replace with the path to your rain GIF
    } else if (lowercaseCondition.includes('cloud')) {
      return 'cloudyy_canva.gif'; // Replace with the path to your cloud GIF
    } else if (lowercaseCondition.includes('clear')) {
      return 'clear_canva.gif'; // Replace with the path to your clear sky GIF
    }
    // Add more conditions for other weather types and corresponding GIFs
  
    return 'clear_canva.gif'; // Default GIF for unknown weather conditions
  };

  const getAdditionalText = (weatherCondition) => {
    if (weatherCondition.toLowerCase().includes('rain')) {
      return "It's going to rain, keep an umbrella!";
    }
    if (weatherCondition.toLowerCase().includes('cloud')) {
        return "Its cloudy, might rain soon , Have a good day!";
      }
    if (weatherCondition.toLowerCase().includes('clear')) {
        return "You can step out without an umbrella , Have a good day!";
      }
    // You can add more conditions for different weather types here

    return ''; // Default text if no condition is met
  };

  return (
    <div className="weather-card">
      <div className="weather-card-content">
        <h3 className="weather-card-title">{title}</h3>
        <p className="weather-card-description">
          {temperature}<br/>
          <br />
          {getAdditionalText(weatherCondition)}
        </p>
        {/* <button className="weather-card-button">{buttonText}</button> */}
      </div>
      <div className="weather-card-image">
        <img src={getWeatherGif(weatherCondition)} alt={title} />
      </div>
    </div>
  );
}

export default WeatherCard;
