document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("season_delivery_cnt");
    const button = document.getElementById("submit-btn");
    const fileInput = document.getElementById("csv-file");
    const fileName = document.getElementById("file-name");
    const form = document.querySelector("form");

    // -----------------------------
    // 1️⃣ 初期状態設定
    // -----------------------------
    updateButtonState();

    // -----------------------------
    // 2️⃣ 入力値によるボタン活性／非活性
    // -----------------------------
    input.addEventListener("input", updateButtonState);

    // ボタン活性・非活性の制御
    function updateButtonState() {
        const isEmpty = input.value.trim() === "";
        button.disabled = isEmpty;

        // 見た目の制御
        if (isEmpty) {
            button.style.backgroundColor = "gray";       // 非活性
            button.style.cursor = "not-allowed";
        } else {
            button.style.backgroundColor = "#8ad36a";    // 活性
            button.style.cursor = "pointer";
        }
    }

    // -----------------------------
    // 3️⃣ CSVファイル選択時のファイル名表示
    // -----------------------------
    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];
        fileName.textContent = file ? file.name : "";
    });

    // -----------------------------
    // 4️⃣ フォーム送信時の動作（確認用）
    // -----------------------------
//     form.addEventListener("submit", (event) => {
//         // ここはデバッグ目的なので、バックエンド連携時は削除してOK
//         event.preventDefault();
//         alert(`送信内容：
// - 配信件数: ${input.value}
// - ファイル名: ${fileInput.files[0] ? fileInput.files[0].name : "なし"}`);
//     });
});
