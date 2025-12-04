document.addEventListener("DOMContentLoaded", () => {
    const labels = JSON.parse(document.getElementById('labels-data').textContent);
    const data = JSON.parse(document.getElementById('chart-data').textContent);

    const ctx = document.getElementById('pieChart');

    // 円グラフの描画の設定
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                // backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
                backgroundColor: [
                    "#171616",
                    "#f5b642",
                    "#87a8e0",
                    "#e3dcda",
                    "#f26405",
                    "#d61313",
                    "#2006c7",
                    "#73726e",
                    "#fcde19",
                    "#f5b642",
                    "#b5a40b",
                    "#383e45",
                    "#56cc49",
                    "#e8a274",
                    "#2b2940"
                ]
            }]
        }
    });
});
