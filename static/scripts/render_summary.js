document.addEventListener('DOMContentLoaded', function() {
    fetchChartData(7);  // Initially fetch for the past 7 days
});


document.querySelectorAll('input[name="dataRange"]').forEach(input => {
    input.addEventListener('change', onChange);
});


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
    const days = document.querySelector('input[name="dataRange"]:checked').value;
    
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

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: true, 
    };

    window.summaryChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(entry => entry.date), 
            datasets: getSelectedDatasets(data)
        },
        options: chartOptions
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
    console.log("resized")
    
    // Set a timeout to trigger the end of the resize event
    resizeTimer = setTimeout(function() {
        // Code to execute after resizing has "stopped"
        if (window.summaryChart) {
            console.log("should be resizing chart")
            window.summaryChart.resize();
        }
    }, 10); 
});

