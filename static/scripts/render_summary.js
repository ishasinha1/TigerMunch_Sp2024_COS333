document.addEventListener('DOMContentLoaded', function() {
    fetchChartData(7);  // Initially fetch for the past 7 days

    // fetch data for the table
    loadMore();

    // create the trends table
    new DataTable('#myTable', {
        paging: false, 
        searching:false,
        info:false,
        responsive: true,
        ordering: false,
    });
});

// adding event listener to change the trends chart when a user
// selects different time windows or nutrition selections
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

// when a user changes selection criteria, we change the chart
function onChange() {
    const days = document.querySelector('input[name="dataRange"]:checked').value;
    
    fetchChartData(days);
}

// when a user wants to see macros, display the macro checkboxes
function toggleMacroSelection() {
    const macroSelectionDiv = document.getElementById('macroSelection');
    if (document.getElementById('macrosChoice').checked) {
        macroSelectionDiv.style.display = 'block';
    } else {
        macroSelectionDiv.style.display = 'none';
    }
}

// use the backend to get the data for the chart
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

// function that creates the chart
function createChart(data) {
    const ctx = document.getElementById('summaryChart').getContext('2d');

    //remove previously existing chart
    if (window.summaryChart instanceof Chart) {
        window.summaryChart.destroy();
    }
    
    // create new charw with new data
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

// select the appropriate datasets from the set of all data
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

// resizing functionality
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

// handles trends table

// uses indices to index pages on the table
let currentPage = 1;
let entriesPerPage = 10;

// function that loads more entries on the summary table
function loadMore() {
    fetch(`/get_summary_table?page=${currentPage}`)
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = '';
        data.forEach(row => {
            const tr = document.createElement('tr');
            // creates new table rows
            tr.innerHTML = `<td class="created_at_year">${row.created_at}</td>
                            <td class="created_at_date">${row.created_at}</td>
                            <td>${row.calories}</td>
                            <td>${row.fat}</td>
                            <td>${row.protein}</td>
                            <td>${row.carbs}</td>`;
            tableBody.appendChild(tr);
        });
        // formats dates appropriately
        formatDates()

        // determines whether the show more button should be displayed
        if (data.length < entriesPerPage * currentPage) {
            const showMoreButton = document.getElementById('show-more-button');
            if (showMoreButton) {
                showMoreButton.style.display = 'none';
            }
                
        }

        // indexes current page
        currentPage++;
    })
    .catch(error => console.error('Error loading more data:', error));

}

// formats dates appropriately
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
