# 🤖 Job Scout Agent

A fully automated job scouting bot that scrapes Machine Learning, Data Science, and AI opportunities across popular platforms and sends you a personalized Excel report daily — right to your inbox!

---

## 📌 Features

- 🔎 Scrapes **StepStone**, **Indeed**, and top **company career pages**:
  - BMW Group
  - Bosch
  - Continental
  - Cyber Valley
  - Mercedes-Benz Group
- 🧠 Categorizes roles into:
  - Internship
  - Working Student
  - Master Thesis
- 📩 Sends job listings as a formatted **Excel file via email**
- 🕕 Runs **daily at 6:00 AM (Germany Time)** using GitHub Actions
- ☁️ Can also run anywhere using **Docker**

---

## 🚀 Quick Start (Local or Docker)

### 🖥️ Run Locally
```bash
pip install -r requirements.txt
python job_agent_ai.py
```

### 🐳 Run in Docker
```bash
docker build -t job-agent .
docker run --env EMAIL_SENDER=your@gmail.com \
           --env EMAIL_PASSWORD=your_app_password \
           --env EMAIL_RECEIVER=your_destination_email \
           job-agent
```

---

## ⚙️ GitHub Actions (Auto-Scheduler)

This repo is configured to run every day via GitHub Actions.

### 📁 `.github/workflows/job_agent.yml`
- Schedules the script at **4:00 UTC / 6:00 CEST**
- Injects your email credentials using GitHub **Secrets**

> To enable this, set the following secrets:

| Secret Name       | Description                       |
|-------------------|-----------------------------------|
| `EMAIL_SENDER`    | Gmail address (must allow SMTP)   |
| `EMAIL_PASSWORD`  | App-specific password from Gmail  |
| `EMAIL_RECEIVER`  | Destination email (e.g. yourself) |

Then go to the **Actions** tab → click **Run workflow** to test.

---

## 🛠 Tech Stack
- Python 3.10
- BeautifulSoup (HTML scraping)
- Requests (HTTP)
- Pandas + OpenPyXL (Excel handling)
- GitHub Actions (CI/CD)
- SMTP (Email automation)

---

## 📬 Output Sample
The email includes an `.xlsx` file like:

| Posted       | Title                         | Company     | Location        | Skills | Matched | Suggestion | Link |
|--------------|-------------------------------|-------------|------------------|--------|---------|------------|------|
| 2025-04-19 06:00 | ML Intern – GenAI | BMW Group | Munich, Germany | ML, LLMs | Python, Llama 3.1 | Mention Llama project | 🔗 |

---

## 💡 Future Features
- GPT-powered skill match
- Export to Notion or Airtable
- Telegram/Slack notifications
- Auto-apply hooks (risky but possible 😄)

---

## 👨‍💻 Created By
**Shalin Vachheta**  
M.Sc. Mechatronics + AI Enthusiast  
🔗 [linkedin.com/in/shalinvachheta](https://linkedin.com/in/shalinvachheta)

---

## 📃 License
MIT License. Use freely, but at your own risk 😉

