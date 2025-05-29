// Count button to calculate average
document.getElementById("countBtn").addEventListener("click", function () {
    const totalGrade = parseFloat(document.getElementById("total_grade").value);
    const totalStudent = parseInt(document.getElementById("total_student").value);

    if (!isNaN(totalGrade) && !isNaN(totalStudent)) {
        if (totalStudent < 90) {
            alert("Number of students must be at least 90.");
            return;
        }

        const avg = totalGrade / totalStudent;

        if (avg > 100) {
            alert("Average grade cannot exceed 100. Please check your inputs.");
            document.getElementById("avg_grade").value = '';
        } else {
            document.getElementById("avg_grade").value = avg.toFixed(2);
        }
    } else {
        alert("Please enter valid numbers for total grade and total students.");
    }
});



document.getElementById("courseForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const jsonData = {
        avg_grade: parseFloat(document.getElementById("avg_grade").value),
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
        document.getElementById("courseForm").reset();
        document.getElementById("avg_grade").value = ""; 
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
            legend: { display: true },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        const x = context.parsed.x;
                        const y = context.parsed.y;
                        return [
                            context.dataset.label,
                            `Average Grade: ${x}`,
                            `Total Student: ${y}`
                        ];
                    }
                }
            }
        },
        scales: {
            x: { title: { display: true, text: 'Average Grade' }, min: 0, max: 100 },
            y: { title: { display: true, text: 'Total Students' }, min: 0 }
        }
    }
});


function updateChart(avg_grade, total_student, cluster) {
    let colorList = ['#FF6384', '#36A2EB', '#FFCE56'];
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

