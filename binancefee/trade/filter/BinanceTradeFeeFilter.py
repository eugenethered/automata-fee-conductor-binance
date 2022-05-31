import logging
from typing import Optional

from binance.error import ClientError
from binance.spot import Spot as Client
from core.number.BigFloat import BigFloat
from core.options.exception.MissingOptionError import MissingOptionError
from coreauth.AuthenticatedCredentials import AuthenticatedCredentials
from coreauth.exception.UnableToAuthenticateError import UnableToAuthenticateError
from fees.trade.filter.TradeFeeFilter import TradeFeeFilter

FEE_FILTER = 'FEE_FILTER'


class BinanceTradeFeeFilter(TradeFeeFilter):

    def __init__(self, options):
        self.log = logging.getLogger(__name__)
        self.options = options
        self.__check_options()
        (self.api_key, self.api_secret) = self.init_auth_credentials()
        self.client = None

    def __check_options(self):
        if self.options is None:
            raise MissingOptionError(f'missing option please provide options {FEE_FILTER}')
        if FEE_FILTER not in self.options:
            raise MissingOptionError(f'missing option please provide option {FEE_FILTER}')

    def init_auth_credentials(self):
        authenticated_credentials = AuthenticatedCredentials(self.options)
        api_key = authenticated_credentials.obtain_auth_value('API_KEY')
        api_secret = authenticated_credentials.obtain_auth_value('API_SECRET')
        return api_key, api_secret

    def lazy_init_client(self):
        if self.client is None:
            self.client = Client(self.api_key, self.api_secret)

    def obtain_account_trade_fee(self) -> Optional[BigFloat]:
        # binance does not provide this at account level, rather for every instrument
        return None

    def obtain_instrument_trade_fee(self, instrument) -> Optional[BigFloat]:
        try:
            self.lazy_init_client()
            instrument_fees = self.client.trade_fee(symbol=instrument)
            if instrument_fees is None or len(instrument_fees) == 0:
                return None
            fees = instrument_fees[0]
            fee = [v for k, v in fees.items() if k.lower() == self.options[FEE_FILTER].lower()]
            if fee is not None and len(fee) > 0:
                return BigFloat(fee[0])
            return None
        except ClientError as binance_client_error:
            self.log.warning(f'Unable to authenticate binance client, error:[{binance_client_error.error_message}]')
            raise UnableToAuthenticateError(binance_client_error.error_message)
