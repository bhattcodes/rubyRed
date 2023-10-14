import React from 'react';
import RedBusCard from './components/chat_card';
import Emergencycard from './components/emergency_card';
// import Weathercard from './components/weather_card';
import ResponseCard from './components/gpt_card';
// import WeatherWidget from './components/weatherwidget';

function App() {
  return (
    <div className="App">
      {/* <WeatherWidget /> */}
      <RedBusCard
        // title="Buddies on the Go"
        description=""
        imageSrc="final_bg.png" // Add the image source
        buttonText="Chat now"
      />
      <Emergencycard
        title="FeelSafe"
        description=""
        // imageSrc="sos_bg" // Add the image source
        buttonText="Safety"
      />
      <ResponseCard
        title="Your Title"
        description="Your Description"
        buttonText="Your Button Text"
        // imageSrc="your-image.jpg" // Path to your image
      />
      {/* <Weathercard
        // title="Weather Forecast"
        description="Check the weather forecast for your destination."
        imageSrc="weather-image.jpg" // Add the image source
        buttonText="Check Weather"
      /> */}
    </div>
  );
}

export default App;
