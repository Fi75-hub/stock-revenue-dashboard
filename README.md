# Stock and Revenue Dashboard

A Python notebook comparing Tesla and GameStop share prices with quarterly revenue. It downloads price history with yfinance, extracts revenue tables with Beautiful Soup, cleans the data with pandas and displays two Plotly charts for each company.

## Run

Use Python 3.10 or later. In this folder, install the dependencies and start JupyterLab:

```sh
python -m pip install -r requirements.txt
python -m pip install jupyterlab
python -m jupyterlab
```

Open `Analyzing_Historical_Stock_Revenue_Data_and_Building_a_Dashboard.ipynb` and run the cells in order. An internet connection is needed for the data downloads. Plotly selects a renderer for the notebook environment.

The notebook reports missing data, unsuccessful downloads and missing revenue tables instead of drawing empty charts. If Yahoo Finance temporarily rejects a request, wait and rerun that cell.

## Data and scope

- Price history comes from Yahoo Finance through [yfinance](https://ranaroussi.github.io/yfinance/). The charts use the `Close` column with automatic price adjustment disabled.
- Quarterly revenue comes from archived Macrotrends pages hosted for the IBM course: [Tesla](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm) and [GameStop](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html).
- Prices are plotted through **14 June 2021** and revenue through **30 April 2021**, following the exercise. The archived revenue tables end on different dates, so their coverage does not match the live price source.
- Dates and revenue amounts are converted to datetime and numeric values before plotting. Revenue is measured in millions of US dollars.

## Tests

The offline tests check revenue cleaning, missing tables, download failures and chart date limits:

```sh
python -m unittest discover -s tests -v
```

## Project context

Completed for IBM's Python Project for Data Science course. The analysis follows its stock-and-revenue exercise and uses the supplied revenue pages. The notebook focuses on data collection, cleaning and visualisation.
