import requests
import pandas as pd
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime
import time

# === CONFIGURATION ===
EMAIL_SENDER = "shalinvachheta2016@gmail.com"
EMAIL_PASSWORD = "zqvb oamk memj aewx"
EMAIL_RECEIVER = "shalin2010vachheta@gmail.com"

# === STEPSTONE SCRAPER ===
def get_stepstone_jobs():
    headers = {"User-Agent": "Mozilla/5.0"}
    queries = ["machine+learning+intern", "data+science+werkstudent", "master+thesis+machine+learning"]
    jobs = []

    for query in queries:
        url = f"https://www.stepstone.de/jobs/{query}.html"

        for attempt in range(3):
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    break
            except requests.exceptions.RequestException as e:
                print(f"[StepStone] Attempt {attempt+1} failed for {url}: {e}")
                time.sleep(2)
        else:
            print(f"[StepStone] StepStone is not responding — skipping...")
            return []  # <-- Don't crash, just skip


        soup = BeautifulSoup(response.content, "html.parser")
        for job_card in soup.select("article[data-at=job-item]")[:10]:
            title = job_card.select_one("h2").get_text(strip=True)
            company = job_card.select_one("div[data-at=job-item-company-name]").get_text(strip=True)
            location = job_card.select_one("div[data-at=job-item-location]").get_text(strip=True)
            link = job_card.find("a", href=True)["href"]
            full_link = f"https://www.stepstone.de{link}"

            jobs.append({
                "Posted": datetime.now().strftime('%Y-%m-%d %H:%M'),
                "Title": title,
                "Company": company,
                "Location": location,
                "Skills": "N/A (Scrape description in future)",
                "Matched": "TBD",
                "Suggestion": "Run LLM skill match (coming soon)",
                "Link": full_link
            })
    return jobs

# === INDEED SCRAPER ===
def get_indeed_jobs():
    headers = {"User-Agent": "Mozilla/5.0"}
    queries = [
        "machine+learning+intern",
        "werkstudent+data+science",
        "master+thesis+artificial+intelligence"
    ]
    jobs = []
    for query in queries:
        url = f"https://de.indeed.com/Jobs?q={query}&l=Germany"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        for card in soup.select("a.tapItem")[:10]:
            title = card.select_one("h2 span").get_text(strip=True)
            company = card.select_one("span.companyName").get_text(strip=True) if card.select_one("span.companyName") else "Unknown"
            location = card.select_one("div.companyLocation").get_text(strip=True) if card.select_one("div.companyLocation") else "Unknown"
            link = "https://de.indeed.com" + card["href"]

            jobs.append({
                "Posted": datetime.now().strftime('%Y-%m-%d %H:%M'),
                "Title": title,
                "Company": company,
                "Location": location,
                "Skills": "N/A (Scrape description in future)",
                "Matched": "TBD",
                "Suggestion": "Run LLM skill match (coming soon)",
                "Link": link
            })
    return jobs

# === COMPANY CAREER PAGES (STATIC LINKS) ===
def get_company_jobs():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    return [
        {
            "Posted": now,
            "Title": "BMW Group – Internship / Thesis / Working Student",
            "Company": "BMW Group",
            "Location": "Germany",
            "Skills": "ML, GenAI, Autonomous Driving",
            "Matched": "Python, PyTorch, LangChain",
            "Suggestion": "Tailor resume for vehicle-focused AI projects",
            "Link": "https://www.bmwgroup.jobs/de/de/schueler-studenten.html"
        },
        {
            "Posted": now,
            "Title": "Bosch AI Internships and Thesis Topics",
            "Company": "Bosch",
            "Location": "Germany",
            "Skills": "Deep Learning, Forecasting, Robotics",
            "Matched": "BiLSTM, Optuna, CV",
            "Suggestion": "Mention your CARLA BiLSTM forecasting project",
            "Link": "https://www.bosch.de/karriere/starten-sie-ihre-karriere/stellenangebote/"
        },
        {
            "Posted": now,
            "Title": "Continental – Working Student / Internship in AI",
            "Company": "Continental",
            "Location": "Germany",
            "Skills": "Computer Vision, Data Analytics",
            "Matched": "CV, Seaborn, Matplotlib",
            "Suggestion": "Showcase your vehicle sales forecasting and visual work",
            "Link": "https://www.continental.com/en/career/jobs/"
        },
        {
            "Posted": now,
            "Title": "Cyber Valley – ML / AI Internships",
            "Company": "Cyber Valley",
            "Location": "Tübingen, Germany",
            "Skills": "LLMs, AI Safety, Foundation Models",
            "Matched": "PEGASUS, Llama 3.1, Hugging Face",
            "Suggestion": "Mention summarization project with SAMSum dataset",
            "Link": "https://cyber-valley.de/en/jobs"
        },
        {
            "Posted": now,
            "Title": "Mercedes-Benz Group – Student Jobs in AI",
            "Company": "Mercedes-Benz",
            "Location": "Germany",
            "Skills": "AI, NLP, Autonomous Systems",
            "Matched": "Transformers, Streamlit, NLP",
            "Suggestion": "Mention Transformer-based NMT project",
            "Link": "https://group.mercedes-benz.com/careers/"
        }
    ]

# === EMAIL SETUP ===
def send_email_with_excel(jobs):
    df = pd.DataFrame(jobs)
    filename = f"job_listings_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    df.to_excel(filename, index=False)

    msg = EmailMessage()
    msg['Subject'] = '🤖 Latest ML/DS Job Listings'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content('Attached are the most recent job listings matching your profile.')

    with open(filename, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=filename)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

# === MAIN WORKFLOW ===
def run_agent():
    stepstone_jobs = get_stepstone_jobs()
    indeed_jobs = get_indeed_jobs()
    company_jobs = get_company_jobs()
    all_jobs = stepstone_jobs + indeed_jobs + company_jobs
    send_email_with_excel(all_jobs)

# Run once (GitHub Actions will handle scheduling)
if __name__ == "__main__":
    run_agent()
