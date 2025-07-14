const tempCtx = document.getElementById("tempChart").getContext("2d");
const humCtx = document.getElementById("humChart").getContext("2d");
const presCtx = document.getElementById("presChart").getContext("2d");

const slider = document.getElementById("timeRangeSlider");
const timeDisplay = document.getElementById("timeDisplay");
const imageSlider = document.getElementById("imageSlider");
const imgElement = document.getElementById("sensorImage");
const imageTimestamp = document.getElementById("imageTimestamp");
const liveToggleButton = document.getElementById("liveToggleButton");
const imageModeStatus = document.getElementById("imageModeStatus");

let imageFiles = [];
let liveImageMode = true;

let isFetchingData = false;
let isFetchingImages = false;

const tempChart = new Chart(tempCtx, {
  type: "line",
  data: {
    labels: [],
    datasets: [{
      label: "Température (°C)",
      data: [],
      borderColor: "rgba(255, 99, 132, 1)",
      backgroundColor: "rgba(255, 99, 132, 0.2)",
      tension: 0.3,
      fill: true,
      pointRadius: 2,
    }],
  },
  options: {
    responsive: true,
    scales: {
      y: { min: 0, max: 50, title: { display: true, text: "°C" } },
      x: { title: { display: true, text: "Time" } },
    },
    plugins: { legend: { display: false } },
  },
});

const humChart = new Chart(humCtx, {
  type: "line",
  data: {
    labels: [],
    datasets: [{
      label: "Humidité (%)",
      data: [],
      borderColor: "rgba(54, 162, 235, 1)",
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      tension: 0.3,
      fill: true,
      pointRadius: 2,
    }],
  },
  options: {
    responsive: true,
    scales: {
      y: { min: 0, max: 100, title: { display: true, text: "%" } },
      x: { title: { display: true, text: "Time" } },
    },
    plugins: { legend: { display: false } },
  },
});

const presChart = new Chart(presCtx, {
  type: "line",
  data: {
    labels: [],
    datasets: [{
      label: "Pression (hPa)",
      data: [],
      borderColor: "rgba(255, 206, 86, 1)",
      backgroundColor: "rgba(255, 206, 86, 0.2)",
      tension: 0.3,
      fill: true,
      pointRadius: 2,
    }],
  },
  options: {
    responsive: true,
    scales: {
      y: { min: 900, max: 1100, title: { display: true, text: "hPa" } },
      x: { title: { display: true, text: "Time" } },
    },
    plugins: { legend: { display: false } },
  },
});

function fetchData() {
  if (isFetchingData) return;
  isFetchingData = true;

  fetch("/data")
    .then((response) => response.json())
    .then((data) => {
      const total = data.temperature.values.length;
      if (slider.max != total) {
        slider.max = total;
        slider.value = total;
      }

      const count = parseInt(slider.value);
      timeDisplay.textContent = `Derniers ${count} points`;

      updateChartData(tempChart, data.temperature, count);
      updateChartData(humChart, data.humidity, count);
      updateChartData(presChart, data.pressure, count);
    })
    .catch((err) => console.error("Erreur fetch:", err))
    .finally(() => {
      isFetchingData = false;
    });
}

function updateChartData(chart, dataset, count) {
  const labels = dataset.timestamps.map((ts) => ts.slice(11, 16));
  chart.data.labels = labels.slice(-count);
  chart.data.datasets[0].data = dataset.values.slice(-count);
  chart.update();
}

function fetchImages() {
  if (isFetchingImages) return;
  isFetchingImages = true;

  fetch("/images")
    .then((response) => response.json())
    .then((files) => {
      imageFiles = files;
      imageSlider.max = files.length;
      if (liveImageMode) imageSlider.value = files.length;
      imageSlider.disabled = liveImageMode || !imageFiles.length;
      if (liveImageMode) displayImage();
    })
    .catch((err) => console.error("Erreur fetch images:", err))
    .finally(() => {
      isFetchingImages = false;
    });
}

function displayImage() {
  if (!imageFiles.length) return;

  const index = Math.max(0, Math.min(imageFiles.length - 1, imageSlider.value - 1));
  const filename = imageFiles[index];

  imgElement.onerror = () => {
    console.error("Erreur chargement image:", imgElement.src);
    imgElement.alt = "Erreur de chargement de l'image";
  };

  imgElement.src = `/static/images/${encodeURIComponent(filename)}`;
  imageTimestamp.textContent = filename.substring(0, 19);
}

function toggleLiveMode() {
  liveImageMode = !liveImageMode;
  updateImageModeUI();
  if (liveImageMode && imageFiles.length) {
    imageSlider.value = imageFiles.length;
    displayImage();
  }
}

function updateImageModeUI() {
  imageSlider.disabled = liveImageMode || !imageFiles.length;
  imageModeStatus.textContent = liveImageMode
    ? "Mode en direct : dernière image affichée automatiquement"
    : "Mode manuel : utilisez le curseur pour naviguer dans les images";
}

slider.addEventListener("change", fetchData);
imageSlider.addEventListener("input", () => {
  if (!liveImageMode) displayImage();
});
liveToggleButton.addEventListener("click", toggleLiveMode);

fetchData();
fetchImages();
updateImageModeUI();

setInterval(fetchData, 5000);
setInterval(() => {
  fetchImages();
}, 5000);
