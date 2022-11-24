from unittest.mock import patch, mock_open

from mercado_bitcoin.ingestors import DataIngestor
from mercado_bitcoin.writers import DataWriter

import datetime
import pytest


'''
@fixture behaviors like @Setup for the tests. Usually is the last of function's parameters
'''
@pytest.fixture
@patch("mercado_bitcoin.ingestors.DataIngestor.__abstractmethods__", set())
def data_ingestor_fixture():
    return DataIngestor(
            coins=['TEST', 'HOW'],
            default_start_date=datetime.date(2022,10,30),
            writer=DataWriter
        )


'''
We're going to need @patch here because we're testing a method from an Abstract Class (ABC)
and that class needs the @abstractmethod ingest to be implemented.
'''
@patch("mercado_bitcoin.ingestors.DataIngestor.__abstractmethods__", set())
class TestIngestors:
    def test_checkpoint_filename(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._checkpoint_filename
        expected = "DataIngestor.checkpoint"
        assert actual == expected


    def test_load_checkpoint_no_checkpoint(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()
        expected = datetime.date(2022, 10, 30)
        assert actual == expected

    '''
    Here we're going to use @patch to mock the python method 'open'


    @patch with mock -> we need to declare this mock in function's test arguments
    '''
    @patch("builtins.open", new_callable=mock_open, read_data="2022-9-15")
    def test_load_checkpoint_existing_checkpoint(self, mock, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()
        expected = datetime.date(2022, 9, 15)
        assert actual == expected


    '''
    Here we're going to use @patch because we don't want to use/activate
    the ._write_checkpoint() - avoiding the creation of .checkpoint file.
    '''
    @patch("mercado_bitcoin.ingestors.DataIngestor._write_checkpoint", return_value=None)
    def test_update_checkpoint_checkpoint_updated(self, mock, data_ingestor_fixture):
        data_ingestor = data_ingestor_fixture
        data_ingestor._update_checkpoint(value=datetime.date(2022, 1, 1))
        actual = data_ingestor._checkpoint
        expected = datetime.date(2022, 1, 1)
        assert actual == expected
    

    @patch("mercado_bitcoin.ingestors.DataIngestor._write_checkpoint", return_value=None)
    def test_update_checkpoint_checkpoint_written(self, mock, data_ingestor_fixture):
        data_ingestor = data_ingestor_fixture
        data_ingestor._update_checkpoint(value=datetime.date(2022, 1, 1))
        mock.assert_called_once()


    '''
    With 2 @patch, we should declare the mock function's parameters in reverse order
    The first @patch should be the last argument
    '''
    @patch("builtins.open", new_callable=mock_open, read_data="2022-10-16")
    @patch("mercado_bitcoin.ingestors.DataIngestor._checkpoint_filename", return_value="foobar.checkpoint")
    def test_write_checkpoint(self, mock_checkpoint_file_name, mock_open_file, data_ingestor_fixture):
        data_ingestor = data_ingestor_fixture
        data_ingestor._write_checkpoint()
        mock_open_file.assert_called_with(mock_checkpoint_file_name, 'w')
