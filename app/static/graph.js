

$(document).ready(function () {
    var scripts = document.getElementById('makeGraph');
    var classification_scores = scripts.getAttribute('classification_scores');
    makeGraph(classification_scores);
    setTimeout(function() {
        //the timeout is to make sure the canvas has the graph plotted before extracting it to download to avoid downloading blank images
        var download_plot_button = document.getElementById("download_plot");
        var canvas = document.getElementById("classificationOutput");
        var image = canvas.toDataURL("image/png");
        download_plot_button.href = image;
    }, 1000);
});

function makeGraph(results) {
    console.log(results);
    results = JSON.parse(results);
    var ctx = document.getElementById("classificationOutput").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: [results[0][0], results[1][0], results[2][0], results[3][0], results[4][0]],
            datasets: [{
                label: 'Output scores',
                data: [results[0][1], results[1][1], results[2][1], results[3][1], results[4][1]],
                backgroundColor: [
                    'rgba(26,74,4,0.8)',
                    'rgba(117,0,20,0.8)',
                    'rgba(121,87,3,0.8)',
                    'rgba(6,33,108,0.8)',
                    'rgba(63,3,85,0.8)',
                ],
                borderColor: [
                    'rgba(26,74,4)',
                    'rgba(117,0,20)',
                    'rgba(121,87,3)',
                    'rgba(6,33,108)',
                    'rgba(63,3,85)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function displayHistogramGraph(histogram_plot) {
    // Append the histogram plot to the specified element
    var histogramOutputElement = document.getElementById('histogramOutput');
    histogramOutputElement.innerHTML = histogram_plot;
}