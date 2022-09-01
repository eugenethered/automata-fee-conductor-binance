FROM python:3.10.6-alpine AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10.6-alpine
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY ./binancefee ./binancefee
ENV PYTHONPATH="${PYTHONPATH}:/app/binancefee"
CMD ["python", "binancefee/__main__.py"]
