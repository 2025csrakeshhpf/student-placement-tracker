FROM python:3.11-slim

WORKDIR /app

# Install g++ so C++ submissions compile inside the container
RUN apt-get update && apt-get install -y --no-install-recommends g++ && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Seed the 720 Coding & Aptitude problems into SQLite during build
RUN python seed_problems.py

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]