// document.getElementById('predictionForm').addEventListener('submit', function(e) {
//     e.preventDefault();

//     const data = {
//         // instructor_id: parseInt(document.getElementById('instructor_id').value),
//         // semester_id: parseInt(document.getElementById('semester_id').value),    
//         // instructor_name: document.getElementById('instructor_name').value,
//         avg_grade: parseFloat(document.getElementById('id_avg_grade').value),
//         avg_score: parseFloat(document.getElementById('id_avg_score').value),
//         avg_attendance: parseFloat(document.getElementById('id_avg_attendance').value)
//     };

//     fetch('predict_instructor/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': getCookie('csrftoken')
//         },
//         body: JSON.stringify(data)
//     })
    
//     .then(response => response.json())
//     .then(result =>{
//         console.log("Prediction result:", result);
//         document.getElementById('statusBox').innerText =
//             `Prediction: ${result.prediction}, Confidence: ${result.probability.map(p => p.toFixed(2)).join(', ')}`;
//         updateChart(result.probability);
//     })
//     .catch(err => {
//         console.error("Error during prediction:", err);
//         document.getElementById('statusBox').innerText = "Error during prediction. Please try again.";
//     });
// });

// function getCookie(name){
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let cookie of cookies){
//             cookie = cookie.trim();
//             if (cookie.startsWith(name + '=')){
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// let predictionChart = null;
// function updateChart(probabilities) {
//     const ctx = document.getElementById('predictionChart').getContext('2d');
//     console.log("Canvas context:", ctx);
//     const labels = probabilities.map((_, index) => `Class ${index}`);
//     const data = {
//         labels: labels, 
//         datasets: [{
//             label: 'Prediction Probabilities',
//             data: probabilities,
//             backgroundColor: ['rgba(75, 192, 192, 0.2)', '#0394BD'],
//             borderColor: ['rgba(75, 192, 192, 1)','#EF39AF'],
//             borderWidth: 1
//         }]
//     };

//     const config = {
//         type: 'bar',
//         data: data,
//         options: {
//             scales: {
//                 y: {
//                     beginAtZero: true,
//                     max: 1,
//                 }
//             },
//         }
//     };

//     if (predictionChart) {
//         predictionChart.data = data;
//         predictionChart.update();
//     }else{
//         predictionChart = new Chart(ctx, config);
//     }
// }

// document.getElementById("predictionForm").addEventListener("submit", function(e){
//     e.preventDefault();

//     const data = {
//         // store_id: parseInt(document.getElementById("id_store_id").value),
//         // active: parseInt(document.getElementById("id_active").value),
//         // total_payment: parseFloat(document.getElementById("id_total_payment").value),
//         // payment_count: parseInt(document.getElementById("id_payment_count").value),
//         // average_payment: parseFloat(document.getElementById("id_average_payment").value)
//         avg_grade: parseFloat(document.getElementById('id_avg_grade').value),
//         avg_score: parseFloat(document.getElementById('id_avg_score').value),
//         avg_attendance: parseFloat(document.getElementById('id_avg_attendance').value)
//     };

//     fetch('/predict-customer/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': getCookie('csrftoken')
//         },
//         body: JSON.stringify(data)
//     })
//     .then(response => response.json())
//     .then(result=>{
//         console.log("prediction result: ", result);
//         document.getElementById("statusBox").innerText=
//             `Prediction: ${result.prediction}, Probabilities: ${result.probability.map(p => p.toFixed(2)).join(', ')}`;
//         updateChart(result.probability);
//     })
//     .catch(err => {
//         console.error('Prediction error:', err);
//         document.getElementById("statusBox").innerText = 'Error making prediction.';
//     });
// });

// function getCookie(name){
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== ''){
//         const cookies = document.cookie.split(';');
//         for (let cookie of cookies){
//             cookie = cookie.trim();
//             if (cookie.startsWith(name + '=')){
//                 cookieValue = decodeURIComponent(cookie.substring(name.length +1));
//                 break;
//             }
//         }
            
//     }
//     return cookieValue;
// }

// let predictionChart = null;
// function updateChart(probabilities){
//     const ctx = document.getElementById('predictionChart').getContext('2d');
//     console.log("Canvas context:", ctx);
//     const labels = probabilities.map((_, index) => `Class ${index}`);
//     const data = {
//         labels: labels,
//         datasets: [{
//             label: 'Probability',
//             data: probabilities,
//             backgroundColor: ['rgba(255, 99, 132, 0.7)', 'rgba(54, 162, 235, 0.7)'],
//             borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)'],
//             borderWidth: 1
//         }]
//     };

//     const config ={
//         type: 'bar',
//         data: data,
//         options: {
//             scales: {
//                 y: {
//                     beginAtZero: true,
//                     max:1
//                 }
//             },
//         }
//     };

//     if (predictionChart){
//         predictionChart.data = data;
//         predictionChart.update();
//     }else{
//         predictionChart = new Chart(ctx, config);
//     }
// }
   

    
// Define cluster display order and custom labels
const clusterInfo = [
    { label: "High", index: 2 },
    { label: "Medium High", index: 1 },
    { label: "Medium Low", index: 0 },
    { label: "Low", index: 3 }
];

document.getElementById("predictionForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const data = {
        avg_grade: parseFloat(document.getElementById('id_avg_grade').value),
        avg_score: parseFloat(document.getElementById('id_avg_score').value),
        avg_attendance: parseFloat(document.getElementById('id_avg_attendance').value)
    };

    fetch('/predict-customer/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(result => {
            console.log("prediction result: ", result);

            const predictedLabel = clusterInfo.find(c => c.index === result.prediction)?.label || `Cluster ${result.prediction}`;
            const formattedProbs = clusterInfo.map(c => `${c.label}: ${result.probability[c.index].toFixed(2)}`).join(', ');

            document.getElementById("statusBox").innerText =
                `Prediction: ${predictedLabel}\nProbabilities: ${formattedProbs}`;

            updateChart(result.probability);
        })
        .catch(err => {
            console.error('Prediction error:', err);
            document.getElementById("statusBox").innerText = 'Error making prediction.';
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

let predictionChart = null;

function updateChart(probabilities) {
    const ctx = document.getElementById('predictionChart').getContext('2d');

    const labels = clusterInfo.map(c => c.label);
    const orderedProbs = clusterInfo.map(c => probabilities[c.index]);

    const data = {
        labels: labels,
        datasets: [{
            label: 'Probability',
            data: orderedProbs,
            backgroundColor: ['rgba(54, 162, 235, 0.7)', 'rgba(255, 99, 132, 0.7)'],
            borderColor: ['rgba(54, 162, 235, 1)', 'rgba(255, 99, 132, 1)'],
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
                    max: 1
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
