FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY job_agent_ai.py .

CMD ["python", "job_agent_ai.py"]
