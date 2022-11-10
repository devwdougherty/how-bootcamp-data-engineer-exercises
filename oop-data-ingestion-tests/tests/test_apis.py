import datetime
import pytest

from apis import DaySummaryApi, TradesApi

class TestDaySummaryApi:

    @pytest.mark.parametrize(
        'coin, date, expected',
        [
            ('BTC', datetime.date(2022, 10, 31), 'https://www.mercadobitcoin.net/api/BTC/day-summary/2022/10/31'),
            ('ETH', datetime.date(2022, 10, 31), 'https://www.mercadobitcoin.net/api/ETH/day-summary/2022/10/31'),
            ('ETH', datetime.date(2019, 1, 2), 'https://www.mercadobitcoin.net/api/ETH/day-summary/2019/1/2')
        ]
    )
    def test_get_endpoint(self, coin, date, expected):
        api = DaySummaryApi(coin=coin)
        actual = api._get_endpoint(date=date)
        assert actual == expected


class TestTradesApi:

    @pytest.mark.parametrize(
        'coin, date_from, date_to, expected',
        [
            ('TEST', datetime.datetime(2022, 10, 28), datetime.datetime(2022, 10, 29), 'https://www.mercadobitcoin.net/api/TEST/trades/1666926000/1667012400'),
            ('TEST', None, None, 'https://www.mercadobitcoin.net/api/TEST/trades'),
            ('TEST', None, datetime.datetime(2020, 11, 17, 0, 0, 1), 'https://www.mercadobitcoin.net/api/TEST/trades'),
            ('TEST', datetime.datetime(2020, 1, 1), None, 'https://www.mercadobitcoin.net/api/TEST/trades/1577847600'),
        ]
    )
    def test_get_endpoint(self, coin, date_from, date_to, expected):
        api = TradesApi(coin=coin)
        actual = api._get_endpoint(date_from=date_from, date_to=date_to)
        assert actual == expected


    def test_get_endpoint_date_from_greater_than_date_to(self):
        with pytest.raises(RuntimeError):
            api = TradesApi(coin='TEST')
            actual = api._get_endpoint(date_from=datetime.datetime(2022, 10, 28), date_to=datetime.datetime(2020, 1, 1))
        
    
    @pytest.mark.parametrize(
        'date, expected',
        [
            (datetime.datetime(2022, 10, 28), 1666926000),
            (datetime.datetime(2022, 10, 29), 1667012400),
            (datetime.datetime(2020, 1, 1), 1577847600),
            (datetime.datetime(2020, 1, 1, 0, 0, 5), 1577847605),
            (datetime.datetime(2021, 11, 17, 0, 0, 1), 1637118001),
        ]
    )
    def test_convert_date_to_unix(self, date, expected):
        api = TradesApi(coin='Test')
        actual = api.convert_date_to_unix(date)
        assert actual == expected

