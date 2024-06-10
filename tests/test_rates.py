import json
import unittest
from unittest.mock import patch, MagicMock

import requests

from tipbot import rates
from .samples import UPDATE


class TestRate(unittest.TestCase):
    def test_get_rate(self):
        rate = rates.get_rate(UPDATE)
        self.assertIsInstance(rate, float)

    def test_get_rate_unsupported_currency(self):
        mock_update = MagicMock()
        rates.get_rate(mock_update, "XYZ")

        mock_update.message.reply_text.assert_called_once_with(
            "XYZ is not a supported currency."
        )

    @patch("tipbot.rates.requests.get")
    def test_get_rate_api_failure(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.RequestException
        mock_update = MagicMock()
        rates.get_rate(mock_update, "USD")

        mock_update.message.reply_text.assert_called_once_with(
            f"Unable to contact {rates.RATE_API}"
        )

    @patch("tipbot.rates.requests.get")
    def test_get_rate_http_error(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.HTTPError
        mock_response = MagicMock()
        mock_response.text = "Error message"
        mock_requests_get.return_value = mock_response
        mock_update = MagicMock()
        rates.get_rate(mock_update, "USD")

        mock_update.message.reply_text.assert_called_once_with(
            f"Unable to contact {rates.RATE_API}"
        )

    @patch("tipbot.rates.requests.get")
    def test_get_rate_parse_failure(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        mock_requests_get.return_value = mock_response
        mock_update = MagicMock()
        rates.get_rate(mock_update, "USD")

        mock_update.message.reply_text.assert_called_once_with(
            f"Unable to parse rate data: {mock_response.text}"
        )
