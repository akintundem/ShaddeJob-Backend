FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY resume_processing.py ./

COPY "Mayokun_Resume.pdf" ./

CMD ["python", "ChatBot.py"]
