import logging

from cache.holder.RedisCacheHolder import RedisCacheHolder
from cache.provider.RedisCacheProviderWithHash import RedisCacheProviderWithHash
from core.environment.EnvironmentVariables import EnvironmentVariables
from logger.ConfigureLogger import ConfigureLogger

from binancefee.BinanceFeeConductor import BinanceFeeConductor


def start():
    ConfigureLogger()

    environment_variables = EnvironmentVariables()

    log = logging.getLogger('Binance Fee Conductor')
    log.info('fee conductor initialized')

    RedisCacheHolder(environment_variables.options, held_type=RedisCacheProviderWithHash)

    conductor = BinanceFeeConductor(environment_variables.options)
    conductor.start_process_schedule()


if __name__ == '__main__':
    start()
