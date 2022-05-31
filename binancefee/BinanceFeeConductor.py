from fees.trade.TradeFeeProvider import TradeFeeProvider
from processmanager.ScheduledProcess import ScheduledProcess

from binancefee.trade.filter.BinanceTradeFeeFilter import BinanceTradeFeeFilter


class BinanceFeeConductor(ScheduledProcess):

    def __init__(self, options):
        super().__init__(options, 'binance', 'fee-conductor')
        self.options = options
        trade_fee_filter = BinanceTradeFeeFilter(options)
        self.trade_fee_provider = TradeFeeProvider(options, trade_fee_filter)

    def process_to_run(self):
        self.trade_fee_provider.obtain_trade_fees()
        self.log.info('Trade Fees call complete')
