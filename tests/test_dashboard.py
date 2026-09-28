import json
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

import pandas as pd
import requests


NOTEBOOK = next(Path(__file__).resolve().parents[1].glob("*.ipynb"))
notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
functions = {}
for cell in notebook["cells"]:
    source = "".join(cell["source"])
    if cell["cell_type"] == "code" and (
        source.startswith("import pandas") or source.startswith("def load_stock")
    ):
        exec(compile(source, str(NOTEBOOK), "exec"), functions)


class DashboardTests(unittest.TestCase):
    def test_revenue_is_numeric_sorted_and_invalid_rows_are_removed(self):
        html = """<table><tr><th>Annual Revenue</th></tr>
            <tr><td>2021</td><td>$99,999</td></tr></table>
            <table><tr><th>Quarterly Revenue (Millions of US $)</th></tr>
            <tr><td>2021-03-31</td><td>$10,389</td></tr>
            <tr><td>2020-12-31</td><td>$9,000</td></tr>
            <tr><td>2020-09-30</td><td></td></tr>
            <tr><td>unknown</td><td>$1,000</td></tr></table>"""
        data = functions["parse_revenue"](html)
        self.assertEqual(data["Revenue"].tolist(), [9000, 10389])
        self.assertTrue(pd.api.types.is_numeric_dtype(data["Revenue"]))
        self.assertEqual(data["Date"].dt.strftime("%Y-%m-%d").tolist(),
                         ["2020-12-31", "2021-03-31"])

    def test_missing_or_empty_quarterly_table_is_reported(self):
        for html in ["<p>Unavailable</p>", "<table><th>Quarterly Revenue</th></table>"]:
            with self.subTest(html=html), self.assertRaises(ValueError):
                functions["parse_revenue"](html)

    def test_http_errors_are_not_parsed_as_data(self):
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("503 unavailable")
        with patch.object(requests, "get", return_value=response) as download:
            with self.assertRaises(requests.HTTPError):
                functions["load_revenue"]("https://example.test/revenue")
            download.assert_called_once_with("https://example.test/revenue", timeout=30)

    def test_empty_stock_download_is_reported(self):
        ticker = Mock()
        ticker.history.return_value = pd.DataFrame()
        with patch.object(functions["yf"], "Ticker", return_value=ticker):
            with self.assertRaisesRegex(ValueError, "No price data"):
                functions["load_stock"]("TSLA")

    def test_chart_uses_date_limits_and_numeric_revenue(self):
        prices = pd.DataFrame({"Date": pd.to_datetime(["2021-06-15", "2021-06-14"]),
                               "Close": [22.0, 21.0]})
        revenue = pd.DataFrame({"Date": pd.to_datetime(["2021-06-30", "2021-03-31"]),
                                "Revenue": [2000, 1000]})
        figure = functions["make_graph"](prices, revenue, "Example")
        self.assertEqual(list(figure.data[0].y), [21.0])
        self.assertEqual(list(figure.data[1].y), [1000])
        self.assertEqual(len(figure.data), 2)
        with self.assertRaisesRegex(ValueError, "date range"):
            functions["make_graph"](prices.iloc[:1], revenue, "Example")


if __name__ == "__main__":
    unittest.main()
