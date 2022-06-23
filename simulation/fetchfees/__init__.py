import logging
import time

from cache.holder.RedisCacheHolder import RedisCacheHolder
from cache.provider.RedisCacheProviderWithHash import RedisCacheProviderWithHash

from binancefee.BinanceFeeConductor import BinanceFeeConductor

if __name__ == '__main__':

    options = {
        'MARKET': 'binance',
        'REDIS_SERVER_ADDRESS': '192.168.1.90',
        'REDIS_SERVER_PORT': 6379,
        'AUTH_INFO_KEY': 'binance:auth:info',
        'PROCESS_KEY': '{}:process:status:{}',
        'PROCESS_RUN_PROFILE_KEY': '{}:process:run-profile:{}',
        'FEE_FILTER': 'takerCommission',
        'ACCOUNT_TRADE_FEE_KEY': 'binance:fee:trade:account',
        'INSTRUMENT_TRADE_FEE_KEY': 'binance:fee:trade:mv:instrument',
        'INSTRUMENT_EXCHANGES_KEY': 'binance:exchange:mv:instruments',
        'VERSION': '0.0.1'
    }

    logging.basicConfig(level=logging.DEBUG)

    RedisCacheHolder(options, held_type=RedisCacheProviderWithHash)

    start_time = time.perf_counter()

    conductor = BinanceFeeConductor(options)
    conductor.run()

    end_time = time.perf_counter()
    print(f"Completed in {end_time - start_time:0.4f} seconds")
