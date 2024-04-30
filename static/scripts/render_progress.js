function renderNutritionChart(canvasId, dailyTotal, goal, label, units) {
    'use strict';
    // only show progress for categories with nonzero goals.
    if (goal == -1 || goal == 0) {
        // Hide the chart and label for this macro counter
        document.getElementById(`${canvasId}Container`).style.display = 'none';

        return; // Exit the function early
    }

    const ctx = document.getElementById(canvasId).getContext('2d');
    const percentageDisplayId = `${canvasId}Percentage`;
    let backgroundColors;
    let dataValues;
    
    if (dailyTotal <= goal) {
        // If daily intake is less than or equal to the goal
        backgroundColors = ['green', 'grey'];
        dataValues = [dailyTotal, goal - dailyTotal];
    } else if(dailyTotal <= goal * 2){;
        backgroundColors = ['orange', 'green'];
        dataValues = [dailyTotal - goal, 2 *goal - dailyTotal];
    } else if(dailyTotal <= goal * 3){
        backgroundColors = ['red', 'orange'];
        dataValues = [dailyTotal - 2*goal, 3 *goal - dailyTotal];
    } else{
        backgroundColors = ['red', 'grey'];
        dataValues = [1, 0];
    }

    const data = {
        datasets: [{
            data: dataValues,
            backgroundColor: backgroundColors,
            borderWidth: 0
        }]
    };
    
    const config = {
        type: 'doughnut',
        data: data,
        options: {
            cutout: '75%',
            // rotation: -90,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    };
    
    new Chart(ctx, config);
    
    // Update the percentage text and label
    const percentage = (dailyTotal / goal) * 100;
    document.getElementById(percentageDisplayId).innerText = `${label}: ${percentage.toFixed(2)}%`;
    
    // Update the label text
    const labelDisplayId = `${canvasId}Label`;
    document.getElementById(labelDisplayId).innerText = `${dailyTotal.toFixed(2)} ${units} / ${goal.toFixed(2)} ${units}`;
}

async function render_chart() {
    const response = await fetch('/nutrition');
    const database_values = await response.json();

    const caloriesGoal = Number(database_values.calorie_goal); // received from the backend
    const dailyCalorieCount = Number(database_values.calories);

    renderNutritionChart('caloriesChart', dailyCalorieCount, caloriesGoal, "Calories", "cal")
    
    const fatGoal = Number(database_values.fat_goal); // received from the backend
    const dailyFatCount = Number(database_values.fat);
    renderNutritionChart('fatChart', dailyFatCount, fatGoal, "Fat", "g")

    const proteinGoal = Number(database_values.protein_goal); // received from the backend
    const dailyProteinCount = Number(database_values.protein);
    renderNutritionChart('proteinChart', dailyProteinCount, proteinGoal, "Protein", "g")

    const carbGoal = Number(database_values.carb_goal); // received from the backend
    const dailyCarbCount = Number(database_values.carbs);
    renderNutritionChart('carbChart', dailyCarbCount, carbGoal, "Carb", "g")  

    if (caloriesGoal == -1 && fatGoal == -1 && proteinGoal == -1 && carbGoal == -1){
        $("#showFeaturesBtn").css("display", "block");
        $("#showFeaturesTxt").css("display", "block");
    }
}

async function render_description() {
    await fetch('/description');
}

document.addEventListener('DOMContentLoaded', render_chart);
document.addEventListener('DOMContentLoaded', render_description);