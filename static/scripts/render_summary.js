document.addEventListener('DOMContentLoaded', function() {
    fetchChartData(7);  // Initially fetch for the past 7 days
});

// Add event listener for any change on radio buttons
document.querySelectorAll('input[name="dataRange"]').forEach(input => {
    input.addEventListener('change', onChange);
});

// Add event listener for any change on radio buttons
document.querySelectorAll('input[name="dataChoice"]').forEach(input => {
    input.addEventListener('change', onChange);
});

document.querySelectorAll('input[name="dataChoice"]').forEach(input => {
    input.addEventListener('change', toggleMacroSelection);
});

document.querySelectorAll('input[name="macro"]').forEach(checkbox => {
    checkbox.addEventListener('change', onChange);
});

function onChange() {
    // Get the value of the selected radio button
    const days = document.querySelector('input[name="dataRange"]:checked').value;
    
    // Fetch and update the chart with the selected range
    fetchChartData(days);
}

function toggleMacroSelection() {
    const macroSelectionDiv = document.getElementById('macroSelection');
    if (document.getElementById('macrosChoice').checked) {
        macroSelectionDiv.style.display = 'block';
    } else {
        macroSelectionDiv.style.display = 'none';
    }
}

function fetchChartData(days) {
    // Modify the endpoint if needed to accept 'all' as a parameter for fetching all data
    const url = days === 'all' ? '/get_summary_values?days=all' : `/get_summary_values?days=${days}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            createChart(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function createChart(data) {
    const ctx = document.getElementById('summaryChart').getContext('2d');

    if (window.summaryChart instanceof Chart) {
        window.summaryChart.destroy();
    }

    window.summaryChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(entry => entry.date), // Your label data
            datasets: getSelectedDatasets(data)
        },
        // options: chartOptions
    });
}

function getSelectedDatasets(data) {
    let datasets = [];

    if (document.getElementById('caloriesChoice').checked) {
        datasets.push({
            label: 'Calories',
            backgroundColor: '#69A593',
            borderColor: '#69A593',
            borderWidth: 10,
            data: data.map(entry => entry.calories),
        });
    } else{
        if (document.getElementById('toggleFat').checked) {
            datasets.push({
                label: 'Fat (in g)',
                data: data.map(entry => entry.fat),
                backgroundColor: '#FFCE56', 
                borderColor: '#FFCE56',
                borderWidth: 5,
            });
        }
    
        if (document.getElementById('toggleProtein').checked) {
            datasets.push({
                label: 'Protein (in g)',
                data: data.map(entry => entry.protein),
                backgroundColor: '#FF0000', 
                borderColor: '#FF0000',
                borderWidth: 5,
            });
        }
    
        if (document.getElementById('toggleCarbs').checked) {
            datasets.push({
                label: 'Carbs (in g)',
                data: data.map(entry => entry.carbs),
                backgroundColor: '#00FF00', 
                borderColor: '#00FF00',
                borderWidth: 5,
            });
        }
    }



    return datasets;
}

let resizeTimer;
window.addEventListener('resize', function() {
    // Clear the timer at the start of resizing
    clearTimeout(resizeTimer);
    
    // Set a timeout to trigger the end of the resize event
    resizeTimer = setTimeout(function() {
        // Code to execute after resizing has "stopped"
        if (window.summaryChart) {
            window.summaryChart.resize();
        }
    }, 10); // You can adjust the timeout duration to suit your needs
});

