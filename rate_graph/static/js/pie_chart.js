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
                data: data, // ← Python で計算した割合
                backgroundColor: colors,
                borderWidth: 2,
            }]
        },
        // 円グラフの内側のラベルの表示
        plugins: [ChartDataLabels],
        options: {
            responsive: false,
            maintainAspectRatio: false,
            
            plugins: {
                // 凡例の表示設定
                legend: {
                    display: true ,
                    position: "top",
                    labels: {
                        font: {size: 20},
                    }
                },
                datalabels: {
                    color: "#fff",
                    align: "center",
                    anchor: "center",
                    formatter: (value, context) => {
                        const label = labels[context.dataIndex];
                        const short_label = label.length > 8 ? label.slice(0, 10) + "…" : label;
                        const percent = value.toFixed(1);   // Python割合をそのまま使用
                        return `${short_label}\n${percent}%`;
                    },
                    // 割合が小さいほどフォントを小さくする
                    font: (ctx) => {
                        const v = data[ctx.dataIndex];
                        
                        // 10%未満 → 小さい
                        if (v < 10) return { size: 7, weight: "bold" };
                        
                        // 20%未満 → 少し小さめ
                        if (v < 20) return { size: 20, weight: "bold"};
                                                
                        // 20%以上 → 標準
                        return { size: 25, weight: "bold" };

                    },
                    padding: 6,
                    clamp: true,             // ← 円の外へ出さない
                    clip: true,              // ← さらに円の内側に収める効果
                }
            },
            // ★★★ クリックイベント ★★★
            onClick: (event, elements) => {
                if (!elements.length) return;
                const index = elements[0].index;  // クリックしたセグメントの index
                const platformName = labels[index];
                
                // 例：画面下に挿入
                const detail = document.getElementById("detail-area");

                // // すでに同じ内容を表示していたらデータ取得しない
                if (detail.dataset.current === platformName) {
                    return;
                } 
                
                //  新しい内容を開く（先にinnerHTMLをリセット）
                detail.innerHTML = "";
                detail.style.display = "block";
                detail.dataset.current = platformName;
                // detail.innerHTML = `<h2>${platformName} の作品</h2>`;
                
                // DjangoのURL呼び出し（GET例）
                fetch(`/rate_graph/platform_info/?platform=${encodeURIComponent(platformName)}`)
                    .then(res => res.text())
                    .then(html => {
                        detail.innerHTML += html;   // HTMLを下に追加
                    });
            }
        }
    });
});
