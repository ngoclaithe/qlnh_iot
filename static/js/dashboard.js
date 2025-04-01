const firebaseConfig = {
  databaseURL: "https://giamsatkholanh-default-rtdb.asia-southeast1.firebasedatabase.app/",
};

firebase.initializeApp(firebaseConfig);
const database = firebase.database();

const tempRef = database.ref('nhietdo');
const humidRef = database.ref('doam');
const tempThresholdRef = database.ref('thresholds/temperature');
const humidThresholdRef = database.ref('thresholds/humidity');
const alertRef = database.ref('alerts');

let tempMinThreshold = 0;
let tempMaxThreshold = 10;
let humidMinThreshold = 40;
let humidMaxThreshold = 70;

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

function formatFullTime(date) {
  return date.toLocaleString();
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

function checkTemperatureThresholds(temperature) {
  if (temperature < tempMinThreshold) {
    addAlert(`Nhiệt độ quá thấp: ${temperature.toFixed(1)}°C (Ngưỡng: ${tempMinThreshold}°C)`, 'critical');
    return 'low';
  } else if (temperature > tempMaxThreshold) {
    addAlert(`Nhiệt độ quá cao: ${temperature.toFixed(1)}°C (Ngưỡng: ${tempMaxThreshold}°C)`, 'critical');
    return 'high';
  }
  return 'normal';
}

function checkHumidityThresholds(humidity) {
  if (humidity < humidMinThreshold) {
    addAlert(`Độ ẩm quá thấp: ${humidity.toFixed(1)}% (Ngưỡng: ${humidMinThreshold}%)`, 'warning');
    return 'low';
  } else if (humidity > humidMaxThreshold) {
    addAlert(`Độ ẩm quá cao: ${humidity.toFixed(1)}% (Ngưỡng: ${humidMaxThreshold}%)`, 'warning');
    return 'high';
  }
  return 'normal';
}

function addAlert(message, level = 'warning') {
  const now = new Date();
  const alertData = {
    time: formatFullTime(now),
    timestamp: now.getTime(),
    message: message,
    level: level
  };
  
  alertRef.push(alertData);
  
  displayAlert(alertData);
}

function displayAlert(alertData) {
  const alertLog = document.getElementById('alert-log');
  const alertItem = document.createElement('div');
  alertItem.className = `alert-item alert-${alertData.level}`;
  
  const alertTime = document.createElement('span');
  alertTime.className = 'alert-time';
  alertTime.textContent = alertData.time;
  
  const alertMessage = document.createElement('span');
  alertMessage.className = 'alert-message';
  alertMessage.textContent = alertData.message;
  
  alertItem.appendChild(alertTime);
  alertItem.appendChild(alertMessage);
  
  alertLog.insertBefore(alertItem, alertLog.firstChild);
  
  if (alertLog.children.length > 100) {
    alertLog.removeChild(alertLog.lastChild);
  }
}

tempRef.on('value', (snapshot) => {
  const temperature = snapshot.val();
  if (temperature !== null) {
    document.getElementById('temperature-value').textContent = temperature.toFixed(1);
    tempGauge.set(temperature);
    
    checkTemperatureThresholds(temperature);
    
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
    
    checkHumidityThresholds(humidity);
    
    const now = new Date();
    addData(humidityChart, formatTime(now), humidity);
    updateTime();
  }
});

tempThresholdRef.on('value', (snapshot) => {
  const thresholds = snapshot.val();
  if (thresholds) {
    tempMinThreshold = thresholds.min;
    tempMaxThreshold = thresholds.max;
    
    document.getElementById('temp-min-threshold').value = tempMinThreshold;
    document.getElementById('temp-max-threshold').value = tempMaxThreshold;
  }
});

humidThresholdRef.on('value', (snapshot) => {
  const thresholds = snapshot.val();
  if (thresholds) {
    humidMinThreshold = thresholds.min;
    humidMaxThreshold = thresholds.max;
    
    document.getElementById('humid-min-threshold').value = humidMinThreshold;
    document.getElementById('humid-max-threshold').value = humidMaxThreshold;
  }
});

alertRef.orderByChild('timestamp').limitToLast(50).on('child_added', (snapshot) => {
  const alertData = snapshot.val();
  displayAlert(alertData);
});

database.ref('.info/connected').on('value', (snapshot) => {
  if (snapshot.val() === false) {
    console.error('Mất kết nối tới Firebase!');
    addAlert('Mất kết nối tới hệ thống giám sát!', 'critical');
  }
});

document.getElementById('save-temp-thresholds').addEventListener('click', () => {
  const minThreshold = parseFloat(document.getElementById('temp-min-threshold').value);
  const maxThreshold = parseFloat(document.getElementById('temp-max-threshold').value);
  
  if (minThreshold >= maxThreshold) {
    alert('Ngưỡng thấp phải nhỏ hơn ngưỡng cao!');
    return;
  }
  
  tempThresholdRef.set({
    min: minThreshold,
    max: maxThreshold
  })
  .then(() => {
    addAlert(`Đã cập nhật ngưỡng nhiệt độ: ${minThreshold}°C - ${maxThreshold}°C`, 'warning');
  })
  .catch((error) => {
    console.error('Lỗi khi lưu ngưỡng nhiệt độ:', error);
    alert('Không thể lưu ngưỡng nhiệt độ!');
  });
});

document.getElementById('save-humid-thresholds').addEventListener('click', () => {
  const minThreshold = parseFloat(document.getElementById('humid-min-threshold').value);
  const maxThreshold = parseFloat(document.getElementById('humid-max-threshold').value);
  
  if (minThreshold >= maxThreshold) {
    alert('Ngưỡng thấp phải nhỏ hơn ngưỡng cao!');
    return;
  }
  
  humidThresholdRef.set({
    min: minThreshold,
    max: maxThreshold
  })
  .then(() => {
    addAlert(`Đã cập nhật ngưỡng độ ẩm: ${minThreshold}% - ${maxThreshold}%`, 'warning');
  })
  .catch((error) => {
    console.error('Lỗi khi lưu ngưỡng độ ẩm:', error);
    alert('Không thể lưu ngưỡng độ ẩm!');
  });
});

document.getElementById('clear-alerts').addEventListener('click', () => {
  if (confirm('Bạn có chắc chắn muốn xóa tất cả cảnh báo?')) {

    alertRef.remove()
      .then(() => {
        document.getElementById('alert-log').innerHTML = '';
        console.log('Đã xóa tất cả cảnh báo');
      })
      .catch((error) => {
        console.error('Lỗi khi xóa cảnh báo:', error);
        alert('Không thể xóa cảnh báo!');
      });
  }
});

updateTime();

tempThresholdRef.once('value', (snapshot) => {
  if (!snapshot.exists()) {
    tempThresholdRef.set({
      min: tempMinThreshold,
      max: tempMaxThreshold
    });
  }
});

humidThresholdRef.once('value', (snapshot) => {
  if (!snapshot.exists()) {
    humidThresholdRef.set({
      min: humidMinThreshold,
      max: humidMaxThreshold
    });
  }
});