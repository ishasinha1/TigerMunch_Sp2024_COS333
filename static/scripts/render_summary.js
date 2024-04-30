document.addEventListener('DOMContentLoaded', function() {
    fetchChartData(7);  // Initially fetch for the past 7 days

    loadMore();

    new DataTable('#myTable', {
        paging: false, 
        searching:false,
        info:false,
        responsive: true,
        ordering: false,
    });
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
    const url = `/get_summary_values?days=${days}`;
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
            labels: data.map(entry => entry.date), 
            datasets: getSelectedDatasets(data)
        },
        options: {
            // chartOptions 
            responsive:true, 
            maintainAspectRatio: false,
            scales: {
                y: { // This targets the y-axis
                    beginAtZero: true, // Ensures the scale starts at zero
                    min: 0 // Explicitly sets the minimum value to 0
                }
            }
        }
    });
}

function getSelectedDatasets(data) {
    let datasets = [];

    if (document.getElementById('caloriesChoice').checked) {
        datasets.push({
            label: 'Calories',
            backgroundColor: '#69A593',
            borderColor: '#69A593',
            borderWidth: 5,
            data: data.map(entry => entry.calories),
        });
    } else{
        if (document.getElementById('toggleFat').checked) {
            datasets.push({
                label: 'Fat (in g)',
                data: data.map(entry => entry.fat),
                backgroundColor: '#FFCE56', 
                borderColor: '#FFCE56',
                borderWidth: 2,
            });
        }
    
        if (document.getElementById('toggleProtein').checked) {
            datasets.push({
                label: 'Protein (in g)',
                data: data.map(entry => entry.protein),
                backgroundColor: '#FF0000', 
                borderColor: '#FF0000',
                borderWidth: 2,
            });
        }
    
        if (document.getElementById('toggleCarbs').checked) {
            datasets.push({
                label: 'Carbs (in g)',
                data: data.map(entry => entry.carbs),
                backgroundColor: '#00FF00', 
                borderColor: '#00FF00',
                borderWidth: 2,
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


let currentPage = 1;
let entriesPerPage = 10;

function loadMore() {
    fetch(`/get_summary_table?page=${currentPage}`)
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = '';
        data.forEach(row => {
            const tr = document.createElement('tr');

            tr.innerHTML = `<td class="created_at_year">${row.created_at}</td>
                            <td class="created_at_date">${row.created_at}</td>
                            <td>${row.calories}</td>
                            <td>${row.fat}</td>
                            <td>${row.protein}</td>
                            <td>${row.carbs}</td>`;
            tableBody.appendChild(tr);
        });
        formatDates()
        if (data.length < entriesPerPage * currentPage) {
            const showMoreButton = document.getElementById('show-more-button');
            if (showMoreButton) {
                showMoreButton.style.display = 'none';
            }
                
        }
        currentPage++;
    })
    .catch(error => console.error('Error loading more data:', error));

}

function formatDates(){
    document.querySelectorAll('.created_at_year').forEach(function(node) {
        const dateParts = node.textContent.trim().split('-');
        const newDate = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]);
        node.textContent = newDate.getFullYear();
    });

    document.querySelectorAll('.created_at_date').forEach(function(node) {
        const dateParts = node.textContent.trim().split('-');
        // Js months are 0 - 11
        const newDate = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]);
        node.textContent = newDate.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric'
        });
    });
}
