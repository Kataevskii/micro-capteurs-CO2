const tempCtx = document.getElementById("tempChart").getContext("2d");
const humCtx = document.getElementById("humChart").getContext("2d");
const presCtx = document.getElementById("presChart").getContext("2d");

const slider = document.getElementById("timeRangeSlider");
const timeDisplay = document.getElementById("timeDisplay");

const tempChart = new Chart(tempCtx, {
  type: "line",
  data: {
    labels: [],
    datasets: [
      {
        label: "Température (°C)",
        data: [],
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        tension: 0.3,
        fill: true,
        pointRadius: 2,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        min: 0,
        max: 50,
        title: { display: true, text: "°C" },
      },
      x: {
        title: { display: true, text: "Time" },
      },
    },
    plugins: {
      legend: { display: false },
    },
  },
});

const humChart = new Chart(humCtx, {
  type: "line",
  data: {
    labels: [],
    datasets: [
      {
        label: "Humidité (%)",
        data: [],
        borderColor: "rgba(54, 162, 235, 1)",
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        tension: 0.3,
        fill: true,
        pointRadius: 2,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        min: 0,
        max: 100,
        title: { display: true, text: "%" },
      },
      x: {
        title: { display: true, text: "Time" },
              },
    },
    plugins: {
      legend: { display: false },
    },
  },
});


const presChart = new Chart(presCtx, {
  type: "line",
  data: {
    labels: [],
    datasets: [
      {
        label: "Pression (hPa)",
        data: [],
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        tension: 0.3,
        fill: true,
        pointRadius: 2,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        min: 900,
        max: 1100,
        title: { display: true, text: "hPa" },
      },
      x: {
        title: { display: true, text: "Time" },
      },
    },
    plugins: {
      legend: { display: false },
    },
  },
});


const samplingIntervalSec = 5;

function fetchData() {
  fetch("/data")
    .then((response) => response.json())
    .then((data) => {
      const tempTimestamps = data.temperature.timestamps;
      const humTimestamps = data.humidity.timestamps;
      const tempValues = data.temperature.values;
      const humValues = data.humidity.values;
      const presTimestamps = data.pressure.timestamps;
      const presValues = data.pressure.values;


      // Tronquer timestamps → HH:MM
      const tempTimestampsShort = tempTimestamps.map((ts) =>
        ts.substring(11, 16)
      );
      const humTimestampsShort = humTimestamps.map((ts) =>
        ts.substring(11, 16)
      );
      const presTimestampsShort = presTimestamps.map((ts) =>
        ts.substring(11, 16)
      );




      const sliderValue = slider.value;
      const totalPoints = tempValues.length;
      const numPoints = Math.max(
        1,
        Math.round(totalPoints * (sliderValue / 100))
      );

      const visibleTempValues = tempValues.slice(-numPoints);
      const visibleTempTimestamps = tempTimestampsShort.slice(-numPoints);

      const visibleHumValues = humValues.slice(-numPoints);
      const visibleHumTimestamps = humTimestampsShort.slice(-numPoints);

      const visiblePresValues = presValues.slice(-numPoints);
      const visiblePresTimestamps = presTimestampsShort.slice(-numPoints);



      tempChart.data.labels = visibleTempTimestamps;
      tempChart.data.datasets[0].data = visibleTempValues;
      tempChart.update();

      humChart.data.labels = visibleHumTimestamps;
      humChart.data.datasets[0].data = visibleHumValues;
      humChart.update();

      presChart.data.labels = visiblePresTimestamps;
      presChart.data.datasets[0].data = visiblePresValues;
      presChart.update();


      updateTimeDisplay(numPoints);
    })
    .catch((err) => console.error("Erreur fetch:", err));
}

function updateTimeDisplay(numPoints) {
  timeDisplay.textContent = `Affichage : ${slider.value}%`;
}

slider.addEventListener("input", fetchData);

let imageFiles = [];

function fetchImages() {
  fetch("/images")
    .then((response) => response.json())
    .then((files) => {
      imageFiles = files;
      updateImageSlider();
      displayImage();
    })
    .catch((err) => console.error("Erreur fetch images:", err));
}

function updateImageSlider() {
  const slider = document.getElementById("imageSlider");
  slider.disabled = imageFiles.length === 0;
}

function displayImage() {
  const slider = document.getElementById("imageSlider");
  if (!imageFiles.length) return;

  const index = Math.max(
    0,
    Math.round(imageFiles.length * (slider.value / 100)) - 1
  );
  let filename = imageFiles[index];

  // Enlève les guillemets en trop, s'il y en a
  filename = filename.replace(/"/g, "");

  const imgElement = document.getElementById("sensorImage");
  imgElement.onerror = () => {
    console.error("Erreur chargement image:", imgElement.src);
    imgElement.alt = "Erreur de chargement de l'image";
  };

  imgElement.src = `/static/images/${encodeURIComponent(filename)}`;

  document.getElementById("imageTimestamp").textContent = filename.substring(
    0,
    19
  );
}

setInterval(fetchData, 5000);
fetchData();
setInterval(fetchImages, 5000);
fetchImages();