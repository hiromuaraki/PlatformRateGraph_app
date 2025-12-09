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
        console.log("loadPlatformInfoの実行");

        // --- フェードアウト ---
        detail.classList.add("fade-out");
        
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
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [{
                data: p_count,
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
                        const index = context.dataIndex;
                        const label = labels[index];
                        const short_label = label.length > 8 ? label.slice(0, 10) + "…" : label;
                        const count = p_count[index];
                        const percent = data[index];
                        return `${short_label}(${count}件)\n${percent}%`;
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
