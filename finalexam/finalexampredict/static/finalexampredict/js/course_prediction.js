document.getElementById("courseForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const jsonData = {
        avg_grade: parseFloat(formData.get("avg_grade")),
        difficulty: parseInt(formData.get("difficulty")),
        total_student: parseInt(formData.get("total_student"))
    };

    fetch("/predict-course-cluster/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": formData.get("csrfmiddlewaretoken")
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.cluster !== undefined) {
            updateChart(jsonData.avg_grade, jsonData.total_student, data.cluster);
        } else {
            alert("Prediction failed.");
        }
    });
});

let chartCtx = document.getElementById("clusterChart").getContext("2d");
let scatterChart = new Chart(chartCtx, {
    type: 'scatter',
    data: {
        datasets: []
    },
    options: {
        plugins: {
            legend: { display: true }
        },
        scales: {
            x: { title: { display: true, text: 'Average Grade' }, min: 0, max: 100 },
            y: { title: { display: true, text: 'Total Students' }, min: 0 }
        }
    }
});

function updateChart(avg_grade, total_student, cluster) {
    let colorList = ['#FF6384', '#36A2EB', '#4BC0C0'];
    let clusterLabels = [
        'Easy & Effective Courses',
        'Hard & Struggling Courses',
        'Potential to Improve Courses'
    ];

    scatterChart.data.datasets.push({
        label: clusterLabels[cluster],
        data: [{ x: avg_grade, y: total_student }],
        backgroundColor: colorList[cluster]
    });
    scatterChart.update();
}

