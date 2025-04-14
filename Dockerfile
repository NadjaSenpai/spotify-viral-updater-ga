FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps chromium

CMD ["python", "update_playlist.py"]