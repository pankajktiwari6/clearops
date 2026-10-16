FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY gateway ./gateway
RUN useradd -r app && chown -R app /srv
USER app
CMD ["uvicorn", "gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
