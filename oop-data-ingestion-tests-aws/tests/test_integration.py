import datetime

from mercado_bitcoin.apis import DaySummaryApi


class TestDaySummaryApi:
    def test_get_data(self):
        actual = DaySummaryApi(coin="BTC").get_data(date=datetime.date(2022, 10, 30))
        expected = {'date': '2022-10-30', 'opening': 109908.9381068, 'closing': 109336, 'lowest': 109000, 'highest': 110856.42107199, 'volume': '3337345.62548023', 'quantity': '30.40577822', 'amount': 2123, 'avg_price': 109760.24363964}
        print(actual)
        assert actual == expected

    
    def test_get_data_better(self):
        actual = DaySummaryApi(coin="BTC").get_data(date=datetime.date(2022, 10, 30)).get("date")
        expected = "2022-10-30"
        print(actual)
        assert actual == expected