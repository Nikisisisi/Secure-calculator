FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
COPY VERSION .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN useradd \
    --system \
    --uid 10001 \
    --create-home \
    --shell /usr/sbin/nologin \
    appuser

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]