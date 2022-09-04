FROM python:3.10.6-alpine AS BUILDER
LABEL stage=BUILDER
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10.6-alpine
RUN addgroup apprunner && adduser apprunner -D -H -G apprunner
USER apprunner
WORKDIR /app
COPY --from=BUILDER /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --chown=apprunner:apprunner ./binancefee ./binancefee

ENV PYTHONPATH="${PYTHONPATH}:/app/binancefee" \
    MARKET=binance \
    REDIS_SERVER_ADDRESS=127.0.0.1 \
    REDIS_SERVER_PORT=6379 \
    AUTH_INFO_KEY=binance:auth:info \
    FEE_FILTER=takerCommission \
    ACCOUNT_TRADE_FEE_KEY=binance:fee:trade:account \
    INSTRUMENT_TRADE_FEE_KEY=binance:fee:trade:mv:instrument \
    INSTRUMENT_EXCHANGES_KEY=binance:exchange:mv:instruments \
    VERSION=0.1 \
    PROCESS_RUN_PROFILE_KEY={}:process:run-profile:{} \
    PROCESS_KEY={}:process:status:{}

CMD ["python", "binancefee/__main__.py"]
