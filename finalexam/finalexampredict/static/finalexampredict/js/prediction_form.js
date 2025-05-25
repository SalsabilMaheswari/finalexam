document.addEventListener("DOMContentLoaded", function() {
    // Initialize chart variable
    let predictionChart = null;
    
    // Form submission handler
    document.getElementById('predictionForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Collect form data
        const data = {
            avg_grade: parseFloat(document.getElementById('id_avg_grade').value),
            avg_score: parseFloat(document.getElementById('id_avg_score').value),
            avg_attendance: parseFloat(document.getElementById('id_avg_attendance').value),
            total_assessment: parseInt(document.getElementById('id_total_assessment').value),
            gpa: parseFloat(document.getElementById('id_gpa').value)
        };

        // Send data to backend
        fetch('/predict-student/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            console.log("Prediction result:", result);
            document.getElementById('statusBox').innerText = 
                `Prediction: ${result.prediction == 1 ? 'Good Performance' : 'Needs Improvement'}, 
                 Probabilities: ${result.probability.map(p => p.toFixed(2)).join(', ')}`;
            updateChart(result.probability);
        })
        .catch(err => {
            console.error('Prediction error:', err);
            document.getElementById('statusBox').innerText = 'Error making prediction.';
        });
    });

    // Function to update chart
    function updateChart(probabilities) {
        const ctx = document.getElementById('predictionChart').getContext('2d');
        const labels = ['Needs Improvement', 'Good Performance'];
        const data = {
            labels: labels,
            datasets: [{
                label: 'Probability',
                data: probabilities,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1
            }]
        };

        const config = {
            type: 'bar',
            data: data,
            options: {
                scales: {
                    y: { 
                        beginAtZero: true,
                        max: 1.0
                    }
                }
            }
        };

        if (predictionChart) {
            predictionChart.data = data;
            predictionChart.update();
        } else {
            predictionChart = new Chart(ctx, config);
        }
    }

    // Function to get CSRF token
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
});

function formatGPAInput() {
    const gpaInput = document.getElementById('id_gpa');
    if (!gpaInput) {
        console.warn('GPA input not found.');
        return;
    }

    gpaInput.addEventListener('input', function () {
        let value = gpaInput.value;

        // Hapus karakter selain angka dan titik
        value = value.replace(/[^0-9.]/g, '');

        // Cegah lebih dari 1 titik
        const parts = value.split('.');
        if (parts.length > 2) {
            value = parts[0] + '.' + parts[1];
        }

        // Maksimal 2 angka di belakang koma
        if (parts.length === 2 && parts[1].length > 2) {
            parts[1] = parts[1].slice(0, 2);
            value = parts[0] + '.' + parts[1];
        }

        // Kalau nilai > 4, bagi 10
        if (parseFloat(value) > 4) {
            value = (parseFloat(value) / 10).toFixed(2);
        }

        gpaInput.value = value;
    });
}
