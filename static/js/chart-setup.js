const ctx = document.getElementById('myChart').getContext('2d');

// Utility function to process data and group it by facility
function processData(data) {
    const facilities = {};

    data.forEach((entry) => {
        if (!facilities[entry.facility]) {
            facilities[entry.facility] = {
                labels: [],
                percentages: [],
                current_occupancies: [],
                max_occupancies: []
            };
        }
        facilities[entry.facility].labels.push(entry.timestamp);
        facilities[entry.facility].percentages.push(parseFloat(entry.percentage.replace('%', '')));
        facilities[entry.facility].current_occupancies.push(entry.current_occupancy);
        facilities[entry.facility].max_occupancies.push(entry.max_occupancy);
    });

    return facilities;
}

// Function to populate facility selector
function populateFacilitySelector(facilities) {
    const selector = document.getElementById('facility-selector');
    // Clear existing options
    selector.innerHTML = '<option value="all">All Facilities</option>';
    // Append new options
    Object.keys(facilities).forEach((facility) => {
        const option = document.createElement('option');
        option.value = facility;
        option.textContent = facility;
        selector.appendChild(option);
    });
}

// Function to fetch data and update the chart
async function fetchDataAndUpdateChart(startDate, endDate, selectedFacility = 'all') {
    try {
        const queryParams = new URLSearchParams();
        if (startDate) queryParams.append('start', startDate);
        if (endDate) queryParams.append('end', endDate);

        const response = await fetch(`/data?${queryParams}`);
        const rawData = await response.json();
        const processedData = processData(rawData);

        const datasets = Object.keys(processedData).map((facility, index) => {
            const hue = 360 * (index / Object.keys(processedData).length); // Different color for each facility
            return {
                label: facility,
                data: processedData[facility].percentages,
                backgroundColor: `hsla(${hue}, 70%, 60%, 0.5)`,
                borderColor: `hsla(${hue}, 70%, 40%, 1)`,
                borderWidth: 2,
                fill: false,
            };
        });

        if (window.myChart && window.myChart.data) {
            window.myChart.data.datasets = datasets;
            window.myChart.update();
        } else {
            window.myChart = new Chart(ctx, {
                type: 'line', // You can also use 'bar' if you prefer
                data: {
                    labels: processedData[Object.keys(processedData)[0]].labels,
                    datasets: datasets
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Occupancy Percentage'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    },
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    plugins: {
                        tooltip: {
                            position: 'nearest',
                            mode: 'index',
                            intersect: false,
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Initial fetch and chart setup
fetchDataAndUpdateChart();

// Set an interval to update the chart regularly
setInterval(fetchDataAndUpdateChart, 900000); // Update every 15 minutes

// Add this at the end of your chart-setup.js
document.getElementById('filter-button').addEventListener('click', function () {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    fetchDataAndUpdateChart(startDate, endDate);
});

