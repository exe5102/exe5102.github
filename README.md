# 停車位預約管理平台 (Parking Reservation System)

這是一個基於 Python Flask 開發的線上停車位預約與管理系統，讓使用者可以透過網頁即時查詢車位狀態、進行預約、報到與模擬繳費；同時提供管理端介面供管理員進行訂單與車位管理。

## 🌟 系統功能特色

### 🚗 客戶端 (Client Side)
*   **車位即時查詢**：整合 Leaflet.js 地圖功能，可即時查看「明秀北路」與「明秀南路」各停車位的目前使用狀態。
*   **線上訂位**：輸入車牌號碼與電話即可快速選擇並預約空車位。
*   **報到功能**：抵達停車場後可透過系統進行報到手續。
*   **訂單查詢與繳費**：輸入車牌號碼即可查詢預約時段、計算應繳金額，並完成線上繳費（模擬）。

### 🛠️ 管理端 (Admin Side)
*   **管理員登入**：安全的身分驗證機制（預設由 `pass.json` 控制）。
*   **總覽儀表板**：一目了然的後台首頁。
*   **訂位資料管理**：可列出所有目前的訂位資料、查詢特定客戶訂單。
*   **取消訂位**：提供強制取消特定車牌號碼訂位的功能。
*   **歷史紀錄查詢**：詳細記錄所有車輛的進出場時間、繳費金額與狀態日誌。

## 💻 技術架構

*   **後端框架**：Python / Flask
*   **資料庫**：SQLite (`Booking.db`)
*   **前端介面**：HTML5, CSS3, JavaScript, jQuery
*   **前端樣板**：使用 [HTML5 UP](https://html5up.net/) 的 Alpha 主題進行客製化與 Jinja2 樣板繼承優化。
*   **地圖整合**：Leaflet.js 與 OpenStreetMap (OSM)

## 🚀 快速開始 (Quick Start)

### 1. 安裝環境依賴
請確保您的系統已安裝 Python 3.x，接著安裝所需的套件：
```bash
pip install Flask pyserial
```

### 2. 啟動伺服器
您可以直接執行專案內附的啟動腳本，或者手動透過 Flask 啟動：

**使用腳本啟動 (Windows):**
```bash
run.cmd
```

**手動啟動:**
```bash
flask run --reload --debugger --host 0.0.0.0 --port 5000
```

### 3. 瀏覽網站
*   **客戶端首頁**: `http://127.0.0.1:5000/`
*   **管理端登入**: `http://127.0.0.1:5000/adminlogin`

## 📁 專案架構說明

```text
/
├── app.py              # Flask 應用程式主程式與路由定義
├── database.py         # 資料庫操作模組 (SQLite 語法與連線)
├── function.py         # 商業邏輯 (費用計算、時間控制、狀態檢查)
├── Booking.db          # SQLite 本機資料庫檔案
├── pass.json           # 管理員帳號密碼設定檔
├── run.cmd             # 快速啟動腳本
├── static/             # 靜態資源 (CSS, JS, 圖片與字體)
└── templates/          # HTML 樣板檔案
    ├── Base.html       # 客戶端共用 Jinja2 版型
    ├── AdminBase.html  # 管理端共用 Jinja2 版型
    └── ...             # 其他功能頁面
```

## 📝 授權聲明 (License)

本專案的前端介面基於 [HTML5 UP](https://html5up.net) 提供的免費開源模板 (Alpha) 修改而來，遵循 CCA 3.0 授權條款。