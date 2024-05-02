function fetchWeatherData() {
  const temperatureHalf = document.querySelector('.temperature-half'); 
  const humidityHalf = document.querySelector('.humidity-half'); 
  fetch('/api/weather')  // Replace with your Flask route to fetch weather data
    .then(response => response.json())
    .then(data => {
      // Update the DOM with the new data
      if(data.temperature){
        document.getElementById('temperatureDate').textContent = data.temperatureDate;
        document.getElementById('temperature').textContent = data.temperature;
      }
      if(data.meanTemperature){//change container color to indicate if it's hot or colr
        if(data.meanTemperature > 23.00)
          temperatureHalf.style.backgroundColor = "#e74c3c";
        else
          temperatureHalf.style.backgroundColor = "#3498db";
        document.getElementById('meanTemperature').textContent = data.meanTemperature;
      }
      if(data.humidity){
        document.getElementById('humidityDate').textContent = data.humidityDate;
        document.getElementById('humidity').textContent = data.humidity;
      }
      if(data.meanHumidity){ //change container color to indicate if it's wet or dry
        if(data.meanHumidity > 40.00)
          humidityHalf.style.backgroundColor = "#87CEEB";
        else
          humidityHalf.style.backgroundColor = "#EDC9AF";
        document.getElementById('meanHumidity').textContent = data.meanHumidity;
      }
    })
    .catch(error => {
      console.error('Error fetching weather data:', error);
    });
}

// Call fetchWeatherData every 5 seconds
setInterval(fetchWeatherData, 5000);
