Chart.defaults.color = '#9A9A9A';
Chart.defaults.font.size = 13;
Chart.defaults.font.family = 'Karla';




// GRÁFICO DE LÍNEAS.

const ctxLine = document.getElementById('line-chart');
let chartData = JSON.parse(document.getElementById('earnings_per_month').textContent);
const allMonths = Array.from(Array(12).keys()).map(function(month) {
    return month + 1;
});

// Llena los meses faltantes con 0.
for (let i = 0; i < allMonths.length; i++) {
    var monthExists = false;
    for (const element of chartData) {
        if (element[0] === allMonths[i]) {
            monthExists = true;
            break;
        }
    }
    if (!monthExists) {
        chartData.push([allMonths[i], 0]);
    }
}

// Ordena los datos por mes.
chartData.sort(function(a, b) {
    return a[0] - b[0];
});

let earnings = chartData.map(function(item) {
    return item[1];
});


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
        labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],

        datasets: [
            {
                label: 'Dinero total obtenido',
                // Axis Y.
                data: earnings,

                // Styles.
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                pointStyle: 'circle',
                pointRadius: 4,
                pointHoverRadius: 13,
                tension: 0.25,
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
        ],
    },

    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Ventas mensuales',
                font: {
                    size: 20,
                }
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
                    callback: function(value, index, ticks) {
                        return '$' + value;
                    }
                },
            },
        },
    },
});




// GRÁFICO CIRCULAR

const ctxPie = document.getElementById('pie-chart');
chartData = JSON.parse(document.getElementById('top_cities').textContent);

let cities = chartData.map(function(item) {
    return item[0];
});

let num_users = chartData.map(function(item) {
    return item[1];
});

const pieChart = new Chart(ctxPie, {
    type: 'doughnut',

    data: {
        labels: cities,

        datasets: [{
            label: 'Top ciudades',
            data: num_users,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
            ],
            borderWidth: 1,
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
                    text: 'Top ciudades',
                    font: {
                        size: 20,
                    }
                },
            },
        },
    }
});




// GRÁFICO DE BARRAS - TOP 5 PRODUCTOS

const ctxBar1 = document.getElementById('bar-chart-1');
chartData = JSON.parse(document.getElementById('top_products').textContent);

let products = chartData.map(function(item) {
    return item[0];
});

let units = chartData.map(function(item) {
    return item[1];
});


const barChart1 = new Chart(ctxBar1, {
    type: 'bar',

    data: {
        labels: products,

        datasets: [{
            label: 'Unidades vendidas',
            data: units,

            // Styles.
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
            ],
            borderWidth: 1,
        }],
    },

    options: {
        responsive: true,
        indexAxis: 'y',
        plugins: {
            title: {
                display: true,
                text: 'Top productos más vendidos',
                font: {
                    size: 20,
                }
            },
        },
    }
});




// GRÁFICO DE BARRAS - TOP 5 CATEGORIAS

const ctxBar2 = document.getElementById('bar-chart-2');
const chartData1 = JSON.parse(document.getElementById('top_categories').textContent);

let categories = chartData1.map(function(item) {
    return item[0];
});

let categories_units = chartData1.map(function(item) {
    return item[1];
});


const barChart2 = new Chart(ctxBar2, {
    type: 'bar',

    data: {
        labels: categories,

        datasets: [
            {
                label: 'Categorías más vendidas',
                data: categories_units,

                // Styles.
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 205, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                ],
                borderColor: [
                    'rgb(255, 99, 132)',
                    'rgb(255, 159, 64)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(54, 162, 235)',
                ],
                borderWidth: 1,
            },
        ],
    },

    options: {
        responsive: true,
        indexAxis: 'y',
        plugins: {
            title: {
                display: true,
                text: 'Top categorias más vendidas',
                font: {
                    size: 20,
                }
            },
        },
    }
});




// GRÁFICO DE BARRAS - TOP 5 MARCAS

const ctxBar3 = document.getElementById('bar-chart-3');
const chartData2 = JSON.parse(document.getElementById('top_brands').textContent);

let brands = chartData2.map(function(item) {
    return item[0];
});

let brands_units = chartData2.map(function(item) {
    return item[1];
});


const barChart3 = new Chart(ctxBar3, {
    type: 'bar',

    data: {
        labels: brands,

        datasets: [
            {
                label: 'Marcas más vendidas',
                data: brands_units,

                // Styles.
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 205, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                ],
                borderColor: [
                    'rgb(255, 99, 132)',
                    'rgb(255, 159, 64)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(54, 162, 235)',
                ],
                borderWidth: 1,
            },
        ],
    },

    options: {
        responsive: true,
        indexAxis: 'y',
        plugins: {
            title: {
                display: true,
                text: 'Top marcas más vendidas',
                font: {
                    size: 20,
                }
            },
        },
    }
});