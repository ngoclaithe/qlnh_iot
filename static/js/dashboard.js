const firebaseConfig = {
    databaseURL: "https://giamsatkholanh-default-rtdb.asia-southeast1.firebasedatabase.app/",
  };
  
  firebase.initializeApp(firebaseConfig);
  const database = firebase.database();
  
  const tempRef = database.ref('nhietdo');
  const humidRef = database.ref('doam');
  
  const tempGauge = new Gauge(document.getElementById('temperature-gauge')).setOptions({
    angle: 0,
    lineWidth: 0.3,
    radiusScale: 1,
    pointer: {
      length: 0.6,
      strokeWidth: 0.035,
      color: '#000000'
    },
    limitMax: false,
    limitMin: false,
    colorStart: '#6FADCF',
    colorStop: '#3498db',
    strokeColor: '#E0E0E0',
    generateGradient: true,
    highDpiSupport: true,
    staticZones: [
      {strokeStyle: "#30B32D", min: -20, max: 0},
      {strokeStyle: "#6FADCF", min: 0, max: 10},
      {strokeStyle: "#FFDD00", min: 10, max: 20},
      {strokeStyle: "#F03E3E", min: 20, max: 40}
    ],
  });
  tempGauge.maxValue = 40;
  tempGauge.setMinValue(-20);
  tempGauge.animationSpeed = 32;
  tempGauge.set(0);
  
  const humidGauge = new Gauge(document.getElementById('humidity-gauge')).setOptions({
    angle: 0,
    lineWidth: 0.3,
    radiusScale: 1,
    pointer: {
      length: 0.6,
      strokeWidth: 0.035,
      color: '#000000'
    },
    limitMax: false,
    limitMin: false,
    colorStart: '#6FADCF',
    colorStop: '#3498db',
    strokeColor: '#E0E0E0',
    generateGradient: true,
    highDpiSupport: true,
    staticZones: [
      {strokeStyle: "#F03E3E", min: 0, max: 20},
      {strokeStyle: "#FFDD00", min: 20, max: 40},
      {strokeStyle: "#30B32D", min: 40, max: 70},
      {strokeStyle: "#6FADCF", min: 70, max: 100}
    ],
  });
  humidGauge.maxValue = 100;
  humidGauge.setMinValue(0);
  humidGauge.animationSpeed = 32;
  humidGauge.set(0);
  
  const temperatureData = {
    labels: [],
    datasets: [{
      label: 'Nhiệt độ (°C)',
      data: [],
      fill: false,
      borderColor: '#3498db',
      tension: 0.1
    }]
  };
  
  const humidityData = {
    labels: [],
    datasets: [{
      label: 'Độ ẩm (%)',
      data: [],
      fill: false,
      borderColor: '#2ecc71',
      tension: 0.1
    }]
  };
  
  const tempCtx = document.getElementById('temperature-chart').getContext('2d');
  const temperatureChart = new Chart(tempCtx, {
    type: 'line',
    data: temperatureData,
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom'
        },
        title: {
          display: true,
          text: 'Biểu đồ nhiệt độ theo thời gian'
        }
      },
      scales: {
        y: {
          beginAtZero: false
        }
      }
    }
  });
  
  const humidCtx = document.getElementById('humidity-chart').getContext('2d');
  const humidityChart = new Chart(humidCtx, {
    type: 'line',
    data: humidityData,
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom'
        },
        title: {
          display: true,
          text: 'Biểu đồ độ ẩm theo thời gian'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100
        }
      }
    }
  });
  
  function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('update-time').textContent = timeString;
  }
  
  function formatTime(date) {
    return date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
  }
  
  function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets[0].data.push(data);
    
    if (chart.data.labels.length > 20) {
      chart.data.labels.shift();
      chart.data.datasets[0].data.shift();
    }
    
    chart.update();
  }
  
  tempRef.on('value', (snapshot) => {
    const temperature = snapshot.val();
    if (temperature !== null) {
      document.getElementById('temperature-value').textContent = temperature.toFixed(1);
      tempGauge.set(temperature);
      
      const now = new Date();
      addData(temperatureChart, formatTime(now), temperature);
      updateTime();
    }
  });
  
  humidRef.on('value', (snapshot) => {
    const humidity = snapshot.val();
    if (humidity !== null) {
      document.getElementById('humidity-value').textContent = humidity.toFixed(1);
      humidGauge.set(humidity);
      
      const now = new Date();
      addData(humidityChart, formatTime(now), humidity);
      updateTime();
    }
  });
  
  database.ref('.info/connected').on('value', (snapshot) => {
    if (snapshot.val() === false) {
      console.error('Mất kết nối tới Firebase!');
    }
  });
  
  updateTime();