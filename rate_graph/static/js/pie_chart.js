document.addEventListener("DOMContentLoaded", () => {
    const labels = JSON.parse(document.getElementById("labels-data").textContent);
    const data = JSON.parse(document.getElementById("chart-data").textContent).map(Number);
    const colors = JSON.parse(document.getElementById("chart-color").textContent);

    const ctx = document.getElementById("pieChart");

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [{
                data: data,                 // ← Python が計算した割合
                backgroundColor: colors,
            }]
        },
        plugins: [ChartDataLabels],
        options: {
            responsive: true,
            maintainAspectRatio: false,
            
            plugins: {
                legend: {
                    position: "right",      // ← 凡例は右側へ（はみ出し防止）
                },
                datalabels: {
                    color: "#fff",
                    align: "center",
                    anchor: "center",
                    formatter: (value, context) => {
                        const label = labels[context.dataIndex];
                        const percent = value.toFixed(1);   // ← Python割合をそのまま使用
                        return `${label}\n${percent}%`;     // ← 2 行表示
                    },
                    font: {
                        size: 25,
                        weight: "bold",
                    },
                    padding: 4,
                    clamp: true,             // ← 円の外へ出さない
                    clip: true,              // ← さらに円の内側に収める効果
                }
            }
        }
    });
});
