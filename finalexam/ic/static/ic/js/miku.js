 let myChart = null;
  let csvData = [];
  const messageBox = document.getElementById('message-box');

  function showMessage(message, type = 'error') {
    messageBox.textContent = message;
    messageBox.style.display = 'block';
    if (type === 'error') {
      messageBox.style.backgroundColor = '#f8d7da';
      messageBox.style.color = '#bb2124';
      messageBox.style.border = '1px solid #f5c2c7';
    } else if (type === 'success') {
      messageBox.style.backgroundColor = '#d1e7dd';
      messageBox.style.color = '#0f5132';
      messageBox.style.border = '1px solid #badbcc';
    } else {
      messageBox.style.backgroundColor = '';
      messageBox.style.color = '';
      messageBox.style.border = '';
    }
  }

  function clearMessage() {
    messageBox.style.display = 'none';
    messageBox.textContent = '';
  }

  // Toggle input fields based on search mode
  const radios = document.querySelectorAll('input[name="search_mode"]');
  const inputIdSemester = document.getElementById('input-id-semester');
  const inputNameSemester = document.getElementById('input-name-semester');

  radios.forEach(radio => {
    radio.addEventListener('change', () => {
      clearMessage();
      if (radio.value === 'id_semester' && radio.checked) {
        inputIdSemester.style.display = 'flex';
        inputNameSemester.style.display = 'none';
      } else if (radio.value === 'name_semester' && radio.checked) {
        inputIdSemester.style.display = 'none';
        inputNameSemester.style.display = 'flex';
      }
    });
  });

  function populateInstructorNames(data) {
    const select = document.getElementById('instructor_name_select');
    select.length = 1; // Clear except placeholder
    const uniqueNames = [...new Set(data.map(d => d.instructor_name).filter(n => n))].sort();
    uniqueNames.forEach(name => {
      const option = document.createElement('option');
      option.value = name;
      option.textContent = name;
      select.appendChild(option);
    });
  }

  window.onload = function() {
    Papa.parse('/static/instructorperf_cluster.csv', {
      download: true,
      header: true,
      dynamicTyping: true,
      complete: function(results) {
        csvData = results.data.filter(row => row.avg_grade !== null && row.avg_score !== null);
        populateInstructorNames(csvData);
        drawScatterPlot(csvData, null, null);
      },
      error: function(err) {
        showMessage("Failed to load clustered data: " + err, 'error');
      }
    });
  };

  document.getElementById('cluster-form').addEventListener('submit', function(event) {
    event.preventDefault();
    clearMessage();

    const searchMode = document.querySelector('input[name="search_mode"]:checked').value;

    if (searchMode === 'id_semester') {
      const instructorId = parseInt(document.getElementById('instructor_id').value);
      const semesterId = parseInt(document.getElementById('semester_id_id').value);

      if (isNaN(instructorId) || isNaN(semesterId)) {
        showMessage("Please enter valid numeric values for both Instructor ID and Semester.", 'error');
        return;
      }

      const match = csvData.find(row => row.instructor_id === instructorId && row.semester_id === semesterId);
      if (!match) {
        showMessage("No matching record found for the specified Instructor ID and Semester. Please check your input and try again.", 'error');
        return;
      }

      drawScatterPlot(csvData, instructorId, semesterId);
      showMessage("Data found and highlighted.", 'success');

    } else if (searchMode === 'name_semester') {
      const instructorName = document.getElementById('instructor_name_select').value.trim().toLowerCase();
      const semesterId = parseInt(document.getElementById('semester_id_name').value);

      if (!instructorName || isNaN(semesterId)) {
        showMessage("Please select an Instructor Name and enter a valid Semester.", 'error');
        return;
      }

      const filtered = csvData.filter(row =>
        row.instructor_name && row.instructor_name.toLowerCase() === instructorName && row.semester_id === semesterId
      );

      if (filtered.length === 0) {
        showMessage("No matching record found for the specified Instructor Name and Semester. Please check your input and try again.", 'error');
        return;
      }

      const first = filtered[0];
      drawScatterPlot(csvData, first.instructor_id, first.semester_id);
      showMessage(`Data found for instructor: ${first.instructor_name}`, 'success');
    }
  });

  document.getElementById('reset-btn').addEventListener('click', function() {
    drawScatterPlot(csvData, null, null);
    document.getElementById('cluster-form').reset();
    clearMessage();
    inputIdSemester.style.display = 'flex';
    inputNameSemester.style.display = 'none';
  });

  // Clear message on input/select change
  ['instructor_id', 'semester_id_id', 'instructor_name_select', 'semester_id_name'].forEach(id => {
    document.getElementById(id).addEventListener('input', clearMessage);
    document.getElementById(id).addEventListener('change', clearMessage);
  });

  function drawScatterPlot(data, highlightInstructorId, highlightSemesterId) {
    const ctx = document.getElementById('myChart').getContext('2d');

    const clusterLabelRemap = {
      '1': '0',
      '3': '1',
      '0': '2',
      '2': '3',
      '4': '4'
    };

    const legendLabels = {
      '0': 'High',
      '1': 'Medium High',
      '2': 'Medium Low',
      '3': 'Low',
      '4': 'Unclustered'
    };

    const clusters = {};
    data.forEach(row => {
      const originalLabel = row.cluster ?? 'Unclustered';
      const remappedLabel = clusterLabelRemap[originalLabel] ?? originalLabel;
      if (!clusters[remappedLabel]) clusters[remappedLabel] = [];
      clusters[remappedLabel].push({
        x: row.avg_grade,
        y: row.avg_score,
        instructor_id: row.instructor_id,
        semester_id: row.semester_id
      });
    });

    const clusterColors = [
      'rgba(255, 99, 132, 0.6)',    // Cluster 0
      'rgba(54, 162, 235, 0.6)',    // Cluster 1
      'rgba(255, 206, 86, 0.6)',    // Cluster 2
      'rgba(75, 192, 192, 0.6)',    // Cluster 3
      'rgba(153, 102, 255, 0.6)'    // Cluster 4
    ];

    const sortedClusterLabels = Object.keys(clusters).sort((a,b) => Number(a) - Number(b));

    const datasets = sortedClusterLabels.map((clusterLabel, idx) => {
      const points = clusters[clusterLabel];
      const legendColor = clusterColors[idx % clusterColors.length]; // warna legend tetap sama

      // Radius tiap titik (besar kalau matching, kecil kalau tidak)
      const pointRadius = points.map(p =>
        p.instructor_id === highlightInstructorId && p.semester_id === highlightSemesterId ? 15:9
      );

      // Warna tiap titik, override merah hanya untuk titik yang dicari kecuali cluster 3
      const pointBackgroundColor = points.map(p => {
        if (
          p.instructor_id === highlightInstructorId &&
          p.semester_id === highlightSemesterId &&
          clusterLabel !== '3' // Kecuali cluster 3, tetap warna legend
        ) {
          return legendColor;
        }
        return legendColor;
      });

      return {
        label: legendLabels[clusterLabel] ||`${clusterLabel}`,
        data: points,
        backgroundColor: legendColor,          // WARNA LEGEND FIXED
        pointBackgroundColor: pointBackgroundColor, // WARNA TITIK SESUAI HIGHLIGHT
        pointRadius: pointRadius
      };
    });

    const xValues = data.map(p => p.avg_grade);
    const yValues = data.map(p => p.avg_score);

    const xMin = Math.min(...xValues) - 5;
    const xMax = Math.max(...xValues) + 5;
    const yMin = Math.min(...yValues) - 5;
    const yMax = Math.max(...yValues) + 5;

    if(myChart) {
      myChart.data.datasets = datasets;
      myChart.options.scales.x.min = xMin;
      myChart.options.scales.x.max = xMax;
      myChart.options.scales.y.min = yMin;
      myChart.options.scales.y.max = yMax;
      myChart.update();
    } else {
      myChart = new Chart(ctx, {
        type: 'scatter',
        data: { datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: { display: true, text: 'Average Grade' },
              min: xMin,
              max: xMax
            },
            y: {
              title: { display: true, text: 'Average Score' },
              min: yMin,
              max: yMax
            }
          },
          plugins: {
            legend: { display: true, position: 'top' },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const p = context.raw;
                  return [
                    `Instructor ID: ${p.instructor_id}`,
                    `Semester ID: ${p.semester_id}`,
                    `Average Grade: ${p.x}`,
                    `Average Score: ${p.y}`
                  ];
                }
              }
            }
          }
        }
      });
    }
  }
