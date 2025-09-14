# 🛡️ Brutalyze Web

**Brutalyze Web** is a lightweight, privacy-focused log analysis web application built with Streamlit that allows users to upload SSH log files and instantly detect:

- 🔐 Failed SSH login attempts  
- 🚨 Brute-force attack patterns  
- 🌍 IP geolocation (country, region, city)  
- 📊 Full log classification (Failed, Successful, Suspicious, Other)

All analysis is done in-memory. No logs are saved on the server, ensuring total user privacy and secure one-click report downloads.

---

## 🌐 Streamlit Cloud Deployment

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

### Deploy to Streamlit Cloud:

1. Fork this repository
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app" and connect your GitHub account
4. Select your forked repository
5. Set the main file path to `streamlit_app.py`
6. Click "Deploy!"

---

## 📁 Project Structure

```
BrutalyzeWeb/
├── streamlit_app.py         # Main Streamlit application
├── brutalyze_core.py        # Core log analysis and classification logic
├── sample_auth.log          # Sample Linux log file (for testing)
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── requirements.txt         # Python dependencies
├── app.py                   # Original Flask app (legacy)
└── templates/               # Original Flask templates (legacy)
```

---

## ⚙️ How to Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/ubiiii/brutalyze-web.git
cd brutalyze-web
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

Visit `http://localhost:8501` in your browser.

---

## 🧪 Try It Out

- Upload your own `auth.log` file
- Or check the box to use the sample file
- View categorized log entries with interactive tables
- Download reports (CSV / JSON / Alerts) securely — no server storage

---

## ✅ Features

- **Interactive Web Interface**: Built with Streamlit for modern UX
- **Real-time Analysis**: Instant log processing and visualization
- **Categorizes all logs into**:
  - 🔴 Failed Login
  - 🟢 Successful Login
  - ⚠️ Suspicious Activity
  - 📄 Other Events
- **Auto-fetches IP geolocation** with country, region, and city data
- **Config-free setup** - works out of the box
- **No user data retained or tracked** - complete privacy
- **Multiple export formats**: CSV, JSON, and Alerts text files
- **Responsive design** - works on desktop and mobile

---

## 🛡️ Privacy First

Brutalyze does **not store** or track uploaded files or results.  
Reports are generated on-demand and never saved on the server.

---

## 📥 Downloadable Reports

| Type    | Description                      |
|---------|----------------------------------|
| CSV     | Full log breakdown by IP/user    |
| JSON    | Full structured response         |
| Alerts  | Only critical flagged items      |

---

## 🚀 Deployment Options

### Streamlit Cloud (Recommended)
- Free hosting for public repositories
- Automatic deployments from GitHub
- Built-in HTTPS and custom domains

### Other Platforms
- **Heroku**: Add `Procfile` with `web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
- **Railway**: Direct deployment from GitHub
- **Render**: Web service deployment
- **Docker**: Use `streamlit` base image

---

## 📸 Screenshots

### Original Flask Version
<img width="1400" height="534" alt="Flask Upload Page" src="https://github.com/user-attachments/assets/a4a7cf4d-a0cd-4812-9349-1944b991576c" />
<img width="1380" height="461" alt="Flask Results Page" src="https://github.com/user-attachments/assets/90265629-2076-4feb-8d66-b0a9777e1ac5" />
<img width="1331" height="795" alt="Flask Analysis Results" src="https://github.com/user-attachments/assets/dd096946-0357-4a2f-9111-d568afe0375d" />
<img width="1358" height="668" alt="Flask Download Options" src="https://github.com/user-attachments/assets/b0e3212d-7587-4954-8543-fcb8683a5b0f" />

### New Streamlit Version
> Screenshots of the modern Streamlit interface coming soon!

---

## 📄 License

MIT License © 2025 [Your Name]
