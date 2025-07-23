# 🛡️ Brutalyze Web

**Brutalyze Web** is a lightweight, privacy-focused log analysis web application that allows users to upload SSH log files and instantly detect:

- 🔐 Failed SSH login attempts  
- 🚨 Brute-force attack patterns  
- 🌍 IP geolocation (country, region, city)  
- 📊 Full log classification (Failed, Successful, Suspicious, Other)

All analysis is done in-memory. No logs are saved on the server, ensuring total user privacy and secure one-click report downloads.

---

## 🌐 Live Demo

> Coming soon — deployable on Replit, Render, Fly.io, or your own server.

---

## 📁 Project Structure

```
BrutalyzeWeb/
├── app.py                   # Flask app with in-memory analysis + downloads
├── brutalyze_core.py        # Core log analysis and classification logic
├── sample_auth.log          # Sample Linux log file (for testing)
├── templates/
│   ├── index.html           # Upload page
│   └── result.html          # Results + download links
├── static/                  # Optional CSS/js
├── uploads/                 # Temporary upload storage
└── requirements.txt         # Python dependencies
```

---

## ⚙️ How to Run

### 1. Clone the repo

```bash
git clone https://github.com/ubiiii/brutalyze-web.git
cd brutalyze-web
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Flask app

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## 🧪 Try It Out

- Upload your own `auth.log` file
- Or check the box to use the sample file
- View categorized log entries
- Download reports (CSV / JSON / Alerts) securely — no server storage

---

## ✅ Features

- Categorizes all logs into:
  - 🔴 Failed Login
  - 🟢 Successful Login
  - ⚠️ Suspicious Activity
  - 📄 Other Events
- Auto-fetches IP geolocation
- Config-free setup
- No user data retained or tracked
- Reports generated only on request and downloaded instantly

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

## 📸 Screenshot
<img width="1400" height="534" alt="image" src="https://github.com/user-attachments/assets/a4a7cf4d-a0cd-4812-9349-1944b991576c" />
<img width="1380" height="461" alt="image" src="https://github.com/user-attachments/assets/90265629-2076-4feb-8d66-b0a9777e1ac5" />
<img width="1331" height="795" alt="image" src="https://github.com/user-attachments/assets/dd096946-0357-4a2f-9111-d568afe0375d" />
<img width="1358" height="668" alt="image" src="https://github.com/user-attachments/assets/b0e3212d-7587-4954-8543-fcb8683a5b0f" />


---

## 📄 License

MIT License © 2025 [Your Name]
