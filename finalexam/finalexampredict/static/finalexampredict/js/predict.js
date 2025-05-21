document.addEventListener("DOMContentLoaded", function () {
    const statusBox = document.getElementById("statusBox");
    const predictionChart = document.getElementById("predictionChart");

    // Example input data - replace with actual input collection
    const inputData = {
        avg_grade: 69.42,
        avg_score: 74.86,
        avg_attendance: 40,
        total_assessment: 36,
        gpa: 3.0
    };

    // Send the data to the backend
    fetch('/predict-student/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputData)
    })
    .then(response => response.json())
    .then(data => {
        // Once the response is received, update the chart with the prediction
        if (data.prediction != undefined) {
            statusBox.textContent = `Prediction: ${data.prediction == 1 ? 'Good Performance' : 'Needs Improvement'}`;
            
            // Create the chart using Chart.js
            new Chart(predictionChart, {
                type: 'bar',
                data: {
                    labels: ['Needs Improvement', 'Good Performance'],
                    datasets: [{
                        label: 'Prediction Probability',
                        data: data.probability,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 1.0
                        }
                    }
                }
            });
        } else {
            statusBox.textContent = 'Error: Could not fetch prediction.';
        }
    })
    .catch(error => {
        statusBox.textContent = 'Error: ' + error.message;
    });
});