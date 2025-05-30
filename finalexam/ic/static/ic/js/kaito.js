// const clusterInfo = [
//     { label: "High", index: 0 },
//     { label: "Medium", index: 1 },
//     { label: "Low", index: 2 }
// ];

// let predictionChart = null;

// document.addEventListener("DOMContentLoaded", function () {
//     const form = document.getElementById("predictionForm");

//     if (!form) {
//         console.error("Form not found!");
//         return;
//     }

//     form.addEventListener("submit", function (e) {
//         e.preventDefault();

//         const data = {
//             num_students: parseInt(document.getElementById('id_num_students').value),
//             avg_attendance: parseFloat(document.getElementById('id_avg_attendance').value),
//             num_A: parseInt(document.getElementById('id_num_A').value),
//             num_B: parseInt(document.getElementById('id_num_B').value),
//             num_C: parseInt(document.getElementById('id_num_C').value),
//             num_D: parseInt(document.getElementById('id_num_D').value)
//         };

//         console.log("Sending data:", data);

//         fetch("/predict-customer/", {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCookie('csrftoken')
//             },
//             body: JSON.stringify(data)
//         })
//         .then(response => response.json())
//         .then(result => {
//             console.log("Prediction result:", result);

//             if (!result || !Array.isArray(result.probability)) {
//                 throw new Error("Invalid prediction result or missing probability array.");
//             }

//             const predictedLabel = clusterInfo.find(c => c.index === result.prediction)?.label || `Cluster ${result.prediction}`;
//             const formattedProbs = clusterInfo.map(c => `${c.label}: ${(result.probability[c.index] * 100).toFixed(2)}%`).join(', ');

//             document.getElementById("statusBox").innerText =
//                 `Prediction: ${predictedLabel}\nProbabilities: ${formattedProbs}`;

//             updateChart(result.probability);
//         })
//         .catch(err => {
//             console.error('Prediction error:', err);
//             document.getElementById("statusBox").innerText = 'Error making prediction.';
//         });
//     });
// });

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let cookie of cookies) {
//             cookie = cookie.trim();
//             if (cookie.startsWith(name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// function updateChart(probabilities) {
//     const ctx = document.getElementById('predictionChart').getContext('2d');
//     if (!ctx) {
//         console.error("Canvas not found!");
//         return;
//     }

//     const labels = clusterInfo.map(c => c.label);
//     const orderedProbs = clusterInfo.map(c => probabilities[c.index] * 100);

//     const chartData = {
//         labels: labels,
//         datasets: [{
//             label: 'Prediction Confidence (%)',
//             data: orderedProbs,
//             backgroundColor: ['#4caf50', '#ff9800', '#f44336'],
//             borderColor: ['#388e3c', '#f57c00', '#d32f2f'],
//             borderWidth: 1
//         }]
//     };

//     const config = {
//         type: 'bar',
//         data: chartData,
//         options: {
//             responsive: true,
//             scales: {
//                 y: {
//                     beginAtZero: true,
//                     max: 100,
//                     title: {
//                         display: true,
//                         text: 'Confidence (%)'
//                     }
//                 }
//             }
//         }
//     };

//     if (predictionChart) {
//         predictionChart.data = chartData;
//         predictionChart.update();
//     } else {
//         predictionChart = new Chart(ctx, config);
//     }
// }

// -------------------------------------------------------

// const clusterInfo = [
//     { label: "High", index: 2 },
//     { label: "Medium", index: 1 },
//     { label: "Low", index: 0 }
// ];

// let predictionChart = null;

// document.addEventListener("DOMContentLoaded", function () {
//     const form = document.getElementById("predictionForm");

//     if (!form) {
//         console.error("Form not found!");
//         return;
//     }

//     // Make sure predictUrl is defined in the HTML <script> tag before this JS file is loaded.
//     if (typeof predictUrl === "undefined") {
//         console.error("predictUrl is not defined. Ensure it is set in a <script> tag before loading kaito.js.");
//         return;
//     }

//     form.addEventListener("submit", function (e) {
//         e.preventDefault();

//         const data = {
//             num_students: parseInt(document.getElementById('id_num_students').value),
//             avg_attendance: parseFloat(document.getElementById('id_avg_attendance').value),
//             num_A: parseInt(document.getElementById('id_num_A').value),
//             num_B: parseInt(document.getElementById('id_num_B').value),
//             num_C: parseInt(document.getElementById('id_num_C').value),
//             num_D: parseInt(document.getElementById('id_num_D').value)
//         };

//         console.log("Sending data:", data);

//         fetch(predictUrl, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCookie('csrftoken')
//             },
//             body: JSON.stringify(data)
//         })
//         .then(response => {
//             if (!response.ok) throw new Error(`Server error: ${response.status}`);
//             return response.json();
//         })
//         .then(result => {
//             console.log("Prediction result:", result);

//             if (!result || !Array.isArray(result.probability)) {
//                 throw new Error("Invalid prediction result or missing probability array.");
//             }

//             const predictedLabel = clusterInfo.find(c => c.index === result.prediction)?.label || `Cluster ${result.prediction}`;
//             const formattedProbs = clusterInfo.map(c => `${c.label}: ${(result.probability[c.index] * 100).toFixed(2)}%`).join(', ');

//             document.getElementById("statusBox").innerText =
//                 `Prediction: ${predictedLabel}\nProbabilities: ${formattedProbs}`;

//             updateChart(result.probability);
//         })
//         .catch(err => {
//             console.error('Prediction error:', err);
//             document.getElementById("statusBox").innerText = 'Error making prediction.';
//         });
//     });
// });

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let cookie of cookies) {
//             cookie = cookie.trim();
//             if (cookie.startsWith(name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// function updateChart(probabilities) {
//     const canvas = document.getElementById('predictionChart');
//     if (!canvas) {
//         console.error("Canvas not found!");
//         return;
//     }

//     const ctx = canvas.getContext('2d');

//     const labels = clusterInfo.map(c => c.label);
//     const orderedProbs = clusterInfo.map(c => probabilities[c.index] * 100);

//     const chartData = {
//         labels: labels,
//         datasets: [{
//             label: 'Prediction Confidence (%)',
//             data: orderedProbs,
//             backgroundColor: ['#4caf50', '#ff9800', '#f44336'],
//             borderColor: ['#388e3c', '#f57c00', '#d32f2f'],
//             borderWidth: 1
//         }]
//     };

//     const config = {
//         type: 'bar',
//         data: chartData,
//         options: {
//             responsive: true,
//             scales: {
//                 y: {
//                     beginAtZero: true,
//                     max: 100,
//                     title: {
//                         display: true,
//                         text: 'Confidence (%)'
//                     }
//                 }
//             }
//         }
//     };

//     if (predictionChart) {
//         predictionChart.data = chartData;
//         predictionChart.update();
//     } else {
//         predictionChart = new Chart(ctx, config);
//     }
// }

// ------------------------


const clusterInfo = [
    { label: "High", index: 2 },
    { label: "Medium", index: 1 },
    { label: "Low", index: 0 }
];

let predictionChart = null;

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("predictionForm");

    if (!form) {
        console.error("Form not found!");
        return;
    }

    // Make sure predictUrl is defined in the HTML <script> tag before this JS file is loaded.
    if (typeof predictUrl === "undefined") {
        console.error("predictUrl is not defined. Ensure it is set in a <script> tag before loading kaito.js.");
        return;
    }

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const data = {
            num_students: parseInt(document.getElementById('id_num_students').value),
            avg_attendance: parseFloat(document.getElementById('id_avg_attendance').value),
            num_A: parseInt(document.getElementById('id_num_A').value),
            num_B: parseInt(document.getElementById('id_num_B').value),
            num_C: parseInt(document.getElementById('id_num_C').value),
            num_D: parseInt(document.getElementById('id_num_D').value)
        };

        console.log("Sending data:", data);

        fetch(predictUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) throw new Error(`Server error: ${response.status}`);
            return response.json();
        })
        .then(result => {
            console.log("Prediction result:", result);

            if (!result || !Array.isArray(result.probability)) {
                throw new Error("Invalid prediction result or missing probability array.");
            }

            const predictedLabel = clusterInfo.find(c => c.index === result.prediction)?.label || `Cluster ${result.prediction}`;
            const formattedProbs = clusterInfo.map(c => `${c.label}: ${(result.probability[c.index] * 100).toFixed(2)}%`).join(', ');
            const accuracyText = result.accuracy ? `\nModel Accuracy: ${(result.accuracy * 100).toFixed(2)}%` : '';

            document.getElementById("statusBox").innerText =
                `Prediction: ${predictedLabel}\nProbabilities: ${formattedProbs}${accuracyText}`;

            updateChart(result.probability);
        })
        .catch(err => {
            console.error('Prediction error:', err);
            document.getElementById("statusBox").innerText = 'Error making prediction.';
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateChart(probabilities) {
    const canvas = document.getElementById('predictionChart');
    if (!canvas) {
        console.error("Canvas not found!");
        return;
    }

    const ctx = canvas.getContext('2d');

    const labels = clusterInfo.map(c => c.label);
    const orderedProbs = clusterInfo.map(c => probabilities[c.index] * 100);

    const chartData = {
        labels: labels,
        datasets: [{
            label: 'Prediction Confidence (%)',
            data: orderedProbs,
            backgroundColor: ['#4caf50', '#ff9800', '#f44336'],
            borderColor: ['#388e3c', '#f57c00', '#d32f2f'],
            borderWidth: 1
        }]
    };

    const config = {
        type: 'bar',
        data: chartData,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Confidence (%)'
                    }
                }
            }
        }
    };

    if (predictionChart) {
        predictionChart.data = chartData;
        predictionChart.update();
    } else {
        predictionChart = new Chart(ctx, config);
    }
}
