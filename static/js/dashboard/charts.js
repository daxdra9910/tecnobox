const ctxLine = document.getElementById('line-chart');
const ctxPie = document.getElementById('pie-chart');
const ctxBar = document.getElementById('bar-chart');


Chart.defaults.color = '#9A9A9A';

Chart.defaults.font.size = 13;
Chart.defaults.font.family = 'Karla';


function gradient(context) {
    const chart = context.chart;
    const {ctx, chartArea} = chart;
    if (!chartArea) { return; }
    let gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
    gradient.addColorStop(0, 'rgba(255, 99, 132, 0.1)');
    gradient.addColorStop(1, 'rgba(255, 0, 0, 0)');
}


const lineChart = new Chart(ctxLine, {
    type: 'line',

    data: {
        // Axis X.
        labels: ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN',
                 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'],

        datasets: [
            {
                label: 'Laptop',
                // Axis Y.
                data: [500, 450, 268, 526, 380, 500, 450, 268, 526, 380, 290, 401],

                // Styles.
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                pointStyle: 'circle',
                pointRadius: 8,
                pointHoverRadius: 13,
                tension: 0.2,
                fill: {
                    target: 'origin',
                    above: function(context) {
                        const chart = context.chart;
                        const {ctx, chartArea} = chart;
                        if (!chartArea) { return; }
                        let gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                        gradient.addColorStop(1, 'rgba(255, 99, 132, 0.25)');
                        gradient.addColorStop(0, 'rgba(255, 0, 0, 0)');
                        return gradient;
                    },
                },
            },
            {
                label: 'Desktop',
                data: [120, 321, 432, 154, 543, 765, 102, 134, 245, 543, 111, 635],

                borderColor: 'rgb(99, 255, 132)',
                backgroundColor: 'rgba(99, 255, 132, 0.5)',
                pointStyle: 'circle',
                pointRadius: 8,
                pointHoverRadius: 13,
                tension: 0.2,
                fill: {
                    target: 'origin',
                    above: function(context) {
                        const chart = context.chart;
                        const {ctx, chartArea} = chart;
                        if (!chartArea) { return; }
                        let gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                        gradient.addColorStop(1, 'rgba(99, 255, 132, 0.25)');
                        gradient.addColorStop(0, 'rgba(0, 255, 0, 0)');
                        return gradient;
                    },
                },
            },
        ],
    },

    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Ventas mensuales por categoría',
            },
        },
        scales: {
            x: {
                border: {
                    display: false,
                },
            },
            y: {
                grid: {
                    display: false,
                },
                ticks: {
                    padding: 15,
                },
            },
        },
    },
});


const pieChart = new Chart(ctxPie, {
    type: 'doughnut',

    data: {
        labels: ['A', 'B', 'C'],

        datasets: [{
            label: 'Top 3 productos más vendidos',
            data: [500, 450, 268],

            // Styles.
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
            ],
            hoverOffset: 4,
        }],
    },

    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    color: 'red',
                },
                title: {
                    display: true,
                    text: 'Top 3 productos más vendidos',
                },
            },
        },
    }
});


const barChart = new Chart(ctxBar, {
    type: 'bar',

    data: {
        labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],

        datasets: [{
            label: 'Ventas por mes',
            data: [500, 450, 268, 640, 321, 120],

            // Styles.
            backgroundColor: 'rgba(255, 159, 64, 0.2)',
            borderColor: 'rgb(255, 159, 64)',
            borderWidth: 1
        }],
    },

    options: {
        responsive: true,
        indexAxis: 'y',
    }
});