import datetime
import pytest
import requests

from unittest.mock import patch

from mercado_bitcoin.apis import DaySummaryApi, TradesApi, MercadoBitcoinApi

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

'''
Using @patch here because we're instantiating an abstract class (ABC). This way our instantiated
abstract class will return a empty set() for us.

@fixture behaviors like @Setup for the tests. Usually is the last of function's parameters
'''
@pytest.fixture()
@patch("mercado_bitcoin.apis.MercadoBitcoinApi.__abstractmethods__", set())
def fixture_mercado_bitcoin_api():
    return MercadoBitcoinApi(
            coin='TEST'
        )


'''
Overriding the requests.get() Response class and behaviors
'''
def mocked_requests_get(*args, **kwargs):
    class MockResponse(requests.Response):
        def __init__(self, json_data, status_code):
            super().__init__()
            self.status_code = status_code # Declaring this because we also want to mock the raise_for_status()
            self.json_data = json_data

        def json(self):
            return self.json_data

        def raise_for_status(self) -> None:
            if self.status_code != 200:
                raise Exception

    if args[0] == "valid_endpoint":
        return MockResponse(json_data={"foo": "bar"}, status_code=200)
    else:   
        return MockResponse(json_data=None, status_code=404)


class TestMercadoBitcoinApi:
    '''
    As we don't want to test/call the real _get_endpoint, requests.get methods, we're using @patch here
    to mock the return of these methods.

    Remember that we always need to send our mocks as function parameters.
    '''
    @patch("requests.get") 
    @patch("mercado_bitcoin.apis.MercadoBitcoinApi._get_endpoint", return_value="valid_endpoint")
    def test_get_data_requests_is_called(self, mock_get_endpoint, mock_requests, fixture_mercado_bitcoin_api):
        fixture_mercado_bitcoin_api.get_data()

        mock_requests.assert_called_once_with("valid_endpoint")

    '''
    Here we're telling (side_effect) that when requests.get is called, we should return our Overriding class implemented
    above, instead the real/mock requests.get
    '''
    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("mercado_bitcoin.apis.MercadoBitcoinApi._get_endpoint", return_value="valid_endpoint")
    def test_get_data_with_valid_endpoint(self, mock_get_endpoint, mock_requests, fixture_mercado_bitcoin_api):
        actual = fixture_mercado_bitcoin_api.get_data()
        expected = {"foo": "bar"}
        assert actual == expected


    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("mercado_bitcoin.apis.MercadoBitcoinApi._get_endpoint", return_value="invalid_endpoint")
    def test_get_data_with_invalid_endpoint(self, mock_get_endpoint, mock_requests, fixture_mercado_bitcoin_api):
        with pytest.raises(Exception):
            fixture_mercado_bitcoin_api.get_data()