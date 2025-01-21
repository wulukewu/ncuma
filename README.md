<div align="center">
  <img src="https://lihi-io.s3.us-west-004.backblazeb2.com/dXNlcl8xNDA4MDc=/1720582168519.png" alt="ncuma Logo" width="300">
</div>

<h1 align="center">ncuma</h1>

<p align="center">
  <strong>截取自<a href="https://w2.math.ncu.edu.tw/">國立中央大學數學系</a>官網，將最新消息傳送至 LINE Notify。</strong>
</p>

---

<h2>目錄</h2>

- [使用說明](#使用說明)
  - [LINE Notify](#line-notify)
  - [新增Google Sheets模版](#新增google-sheets模版)
  - [Google Sheets API](#google-sheets-api)
- [參考資料](#參考資料)

## 使用說明
請依照以下步驟將<code>LINE_NOTIFY_ID</code>、<code>DISCORD_TOKEN</code>、<code>DISCORD_GUILD_ID</code>、<code>DISCORD_CHANNEL_ID</code>、<code>GOOGLE_SHEETS_KEY</code>、<code>GS_CREDENTIALS</code>三個Secrets儲存在GitHub當中。<br>
Fork → Create Fork → Settings → Secrets and variables → Actions → New repository secret<br>
Actions → I understand my workflows, go ahead and enable them → Enable workflow


#### [LINE Notify](https://notify-bot.line.me/)
1. <code>LINE_NOTIFY_ID</code>：如果有多個，可以用空格分開<br><br>
   Steps:<br>
   個人頁面 → 發行權杖<br><br>
   > Example:
   > ```
   > LINE_NOTIFY_ID_1 LINE_NOTIFY_ID_2
   > ```


#### [Discord Developer Portal](https://discord.com/developers/applications)
2. <code>DISCORD_TOKEN</code>、<code>DISCORD_GUILD_ID</code>、<code>DISCORD_CHANNEL_ID</code>：邀請BOT至群組內，並取得BOT的`DISCORD_TOKEN`及群組的`DISCORD_GUILD_ID`、`DISCORD_CHANNEL_ID`。


#### [新增Google Sheets模版](https://lihi.cc/y0vet)
3. <code>GOOGLE_SHEETS_KEY</code>：在`https://docs.google.com/spreadsheets/d/`後的一串金鑰<br><br>
   Steps: <br>
   建立副本 → 複製Google Sheets Key<br><br>
   > Example:
   > ```
   > 1qg59GfsNuiWMCaqrd3pvDVyBl6o3ZC25VA9my01i0WE
   > ```


#### [Google Sheets API](https://console.cloud.google.com/apis/dashboard)
4. <code>GS_CREDENTIALS</code>：複製JSON當中所有的內容<br><br>
   Steps: 
   - 建立專案：選取專案 → 新增專案
   - 啟用 Google Sheets API：ENABLE APPS AND SERVICES → Google Sheets API → 啟用
   - 新增憑證：憑證 → 建立憑證 → 服務帳戶 → 繼續 → 完成（至Google Sheets共用此服務帳號）
   - 新增金鑰：點擊服務帳戶 → 新增金鑰 → 建立新的金鑰 → JSON
<br><br>
   > Example:
   > ```
   > {
   >   "type": "service_account",
   >   "project_id": "PROJECT_ID",
   >   "private_key_id": "PRIVATE_KEY_ID",
   >   "private_key": "-----BEGIN PRIVATE KEY-----PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
   >   "client_email": "CLIENT_EMAIL",
   >   "client_id": "CLIENT_ID",
   >   "auth_uri": "AUTH-URI",
   >   "token_uri": "TOKEN_URI",
   >   "auth_provider_x509_cert_url": "AUTH_PROVIDER_X509_CERT_URL",
   >   "client_x509_cert_url": "CLIENT_X509_CERT_URL"
   > }
   > ```

## 參考資料

以下是一些撰寫程式時參考的網站：

- [Python Line Notify](https://www.learncodewithmike.com/2020/06/python-line-notify.html)
- [Selenium AttributeError解決方法](https://stackoverflow.com/questions/72854116/selenium-attributeerror-webdriver-object-has-no-attribute-find-element-by-cs)
- [Pandas and Google Sheets](https://www.learncodewithmike.com/2021/06/pandas-and-google-sheets.html)
- [Python 讀寫 Google Sheets 教學](https://hackmd.io/@Yun-Cheng/GoogleSheets)
- [ChromeDriver for Testing](https://googlechromelabs.github.io/chrome-for-testing/)
- [ChromeDriver - CNPM Binaries Mirror](https://registry.npmmirror.com/binary.html?path=chromedriver)
- [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
- [python一行命令安装chromedriver](https://www.cnblogs.com/wxhou/p/chromedriver-py.html)
- [Python 項目調用 Github Actions 中的 Secrets](https://ivitan.com/posts/GithubSecret.html)
