fetch('data/graph_data.json')
  .then(response => response.json())
  .then(data => {
    const ctx1 = document.getElementById('chart1').getContext('2d');
    const ctx2 = document.getElementById('chart2').getContext('2d');
    const ctx3 = document.getElementById('chart3').getContext('2d');
    
    // Create chart for Graph 1
    const chart1 = new Chart(ctx1, {
      type: 'line',
      data: {
        labels: data.graph1.labels,
        datasets: [{
          label: 'Graph 1',
          data: data.graph1.data,
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }]
      },
      options: { 
        scales: { 
          y: { 
            beginAtZero: true 
          } 
        },
        title: {
          display: true,
          text: 'Graph 1'
        }
      }
    });
    
    // Create chart for Graph 2
    const chart2 = new Chart(ctx2, {
      type: 'line',
      data: {
        labels: data.graph2.labels,
        datasets: [{
          label: 'Graph 2',
          data: data.graph2.data,
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }]
      },
      options: { 
        scales: { 
          y: { 
            beginAtZero: true 
          } 
        },
        title: {
          display: true,
          text: 'Graph 2'
        }
      }
    });
    
    // Create chart for Graph 3
    const chart3 = new Chart(ctx3, {
      type: 'line',
      data: {
        labels: data.graph3.labels,
        datasets: [{
          label: 'Graph 3',
          data: data.graph3.data,
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1
        }]
      },
      options: { 
        scales: { 
          y: { 
            beginAtZero: true 
          } 
        },
        title: {
          display: true,
          text: 'Graph 3'
        }
      }
    });
  });
