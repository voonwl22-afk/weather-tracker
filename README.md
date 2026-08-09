# 每日天气数据自动抓取

使用 [Open-Meteo](https://open-meteo.com/) 免费 API（无需申请 Key），每天自动抓取一次天气数据，
以追加行的方式写入 `data/weather_history.csv`，并由 GitHub Actions 自动提交回仓库。

默认抓取地点：**Bukit Mertajam, Penang, MY**（可在 `fetch_weather.py` 顶部修改）。

## 部署步骤（5 分钟搞定）

1. 在 GitHub 上新建一个仓库（Public 或 Private 都可以）。
2. 把本文件夹的全部内容上传 / push 到该仓库根目录，目录结构保持不变：
   ```
   your-repo/
   ├── .github/workflows/daily-weather.yml
   ├── fetch_weather.py
   ├── requirements.txt
   └── data/                 （首次运行后会自动生成 weather_history.csv）
   ```
3. 进入仓库的 **Settings → Actions → General**，把 "Workflow permissions" 设置为
   **"Read and write permissions"**（否则 Actions 无法把抓到的数据提交回仓库）。
4. 进入 **Actions** 标签页，找到 "每日天气数据抓取" 这个 workflow，
   点击 **Run workflow** 手动跑一次，确认能成功抓取并生成 `data/weather_history.csv`。
5. 之后它会按 cron 设定的时间（默认每天马来西亚时间早上 8 点，即 UTC 0 点）自动运行，
   数据会不断追加到同一个 CSV 文件里，你可以随时在 GitHub 上打开这个文件查看历史记录。

## 自定义

- **修改地点**：编辑 `fetch_weather.py` 顶部的 `LOCATION_NAME` / `LATITUDE` / `LONGITUDE`。
- **修改抓取时间**：编辑 `.github/workflows/daily-weather.yml` 里的 `cron` 表达式
  （cron 使用 UTC 时间，注意与本地时区换算）。
- **修改抓取字段**：`fetch_weather.py` 里的 `params` 和 `row` 部分，Open-Meteo 支持
  的全部字段可查看官方文档 https://open-meteo.com/en/docs 。

## 注意

- GitHub Actions 的免费额度（Public 仓库无限免费；Private 仓库每月有一定免费分钟数）
  足够支撑每天一次的抓取任务，几乎不会产生费用。
- 如果想要"抓到数据后发送通知"（比如发邮件、Telegram、微信），可以在
  `fetch_weather.py` 里追加对应的推送逻辑，需要的话告诉我，我再帮你加上。
