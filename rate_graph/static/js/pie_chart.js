document.addEventListener("DOMContentLoaded", () => {
    // 例：画面下に挿入
    const detail = document.getElementById("detail-area");
    const labels = JSON.parse(document.getElementById("labels-data").textContent);
    const data = JSON.parse(document.getElementById("chart-data").textContent).map(Number);
    const colors = JSON.parse(document.getElementById("chart-color").textContent);
    const p_count = JSON.parse(document.getElementById("chart-p_count").textContent);

    const ctx = document.getElementById("pieChart");

    // 先に読み込んでページ遷移しないようにしている
    setupPaginationEvents();
    
    // DjangoのURL呼び出し（GET例）
    function loadPlatformInfo(platformName, page = 1) {

        // --- フェードアウト ---
        detail.classList.add("fade-out");
        // 非同期処理（WebAPIを利用しPython側のviews.pygからデータ結果を受け取っている）※Ajaxではない
        fetch(`/rate_graph/platform_info/?platform=${encodeURIComponent(platformName)}&page=${page}`)
            .then(res => res.text())
            .then(html => {
                
                setTimeout(() => {
                    detail.innerHTML = html;   // ページ切り替えなので = にするほうが自然

                    // ページネーション再設定
                    setupPaginationEvents();

                    // フェードイン
                    detail.classList.remove("fade-out");

                }, 200); // CSSと合わせて200〜250ms
            });
    }

    // ★ページネーションのリンクでページ遷移しないように制御
    // Ajaxのページネーションのリンク時に必要
    function setupPaginationEvents() {
        document.querySelectorAll("#detail-area .page-link").forEach(a => {
            a.addEventListener("click", function(e) {
                e.preventDefault();  // 本来のページ遷移を止める
            
                const url = new URL(this.href);
                const page = url.searchParams.get("page");
                const platform = detail.dataset.current;
                console.log(detail);
            
                loadPlatformInfo(platform, page);
            });
        });
    }

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 1,
                barThickness: 40,        // ← 固定幅（px）
                maxBarThickness: 50,     // ← 最大幅
                categoryPercentage: 0.7,// ← カテゴリ幅に対する割合
                barPercentage: 0.9,     // ← その中での棒の割合
            }]
            },
            // 棒グラフの内側のラベルの表示
            plugins: [ChartDataLabels],
            options: {
                responsive: false,
                maintainAspectRatio: false,

                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: (value) => value + "%"
                        },
                        title: {
                            display: true,
                            text: "配信比率（%）"
                        }
                    },
                    x: {
                        ticks: {
                            font: { size: 11 }
                        }
                    }
                },

                plugins: {
                legend: {
                    display: false,
                },
                datalabels: {
                    anchor: "end",
                    align: "top",
                    color: "#000",
                    formatter: (value, context) => {
                        const index = context.dataIndex;
                        const count = p_count[index];
                        return `${value}%\n(${count}件)`;
                    },
                    font: {
                        size: 15,
                        weight: "bold"
                    }
                }
            },
            // ★★★ クリックイベント ★★★
            onClick: (event, elements) => {
                if (!elements.length) return;
                const index = elements[0].index;  // クリックしたセグメントの index
                const platformName = labels[index];

                //すでに同じ内容を表示していたらデータ取得しない
                if (detail.dataset.current === platformName) {
                    setTimeout(() => {
                        detail.scrollIntoView({ behavior: "smooth", block: "start" });
                    }, 50);
                    return;
                } 
                detail.style.display = "block";
                detail.dataset.current = platformName;
                // 初回ロードは1ページ目を表示
                loadPlatformInfo(platformName);

                setTimeout(() => {
                    detail.scrollIntoView({ behavior: "smooth", block: "start" });
                }, 300);  // フェードアウト→フェードインに少し時間を合わせる
            }
        }
    });
});
