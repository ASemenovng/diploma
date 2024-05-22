


































































import pandas as pd
import numpy as np
from datetime import datetime


def process_and_assign_tickers_to_quantiles_quarterly(file_name):
    with pd.ExcelFile(file_name) as xls:
        sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

    quantiles = {0.2: {}, 0.4: {}, 0.6: {}, 0.8: {}}
    portfolios = {q: {} for q in range(5)}  

    quarterly_months = ['-01', '-04', '-07', '-10']
    all_data = {}

    for sheet_name, data in sheets_dict.items():
        quarterly_data = data[data['year_month'].str[-3:].isin(quarterly_months)]
        for index, row in quarterly_data.iterrows():
            year_month = row['year_month']
            capitalization = row['capitalization']

            if year_month not in all_data:
                all_data[year_month] = []
            all_data[year_month].append((sheet_name, capitalization))

    
    for date, entries in all_data.items():
        caps = [entry[1] for entry in entries]
        if caps:
            sorted_caps = sorted(caps)
            quantile_values = {
                0.2: np.percentile(sorted_caps, 20),
                0.4: np.percentile(sorted_caps, 40),
                0.6: np.percentile(sorted_caps, 60),
                0.8: np.percentile(sorted_caps, 80)
            }
            quantiles = {
                0.2: quantile_values[0.2],
                0.4: quantile_values[0.4],
                0.6: quantile_values[0.6],
                0.8: quantile_values[0.8]
            }

            for q in portfolios:
                portfolios[q][date] = []

            for sheet_name, cap in entries:
                if cap < quantiles[0.2]:
                    portfolios[0][date].append(sheet_name)
                elif quantiles[0.2] <= cap < quantiles[0.4]:
                    portfolios[1][date].append(sheet_name)
                elif quantiles[0.4] <= cap < quantiles[0.6]:
                    portfolios[2][date].append(sheet_name)
                elif quantiles[0.6] <= cap < quantiles[0.8]:
                    portfolios[3][date].append(sheet_name)
                elif cap >= quantiles[0.8]:
                    portfolios[4][date].append(sheet_name)

    return portfolios


file_name = '../data/filtered_blue_chips (2).xlsx'
portfolios = process_and_assign_tickers_to_quantiles_quarterly(file_name)


print("Quarterly Portfolios based on capitalization quantiles:")
for i, q in enumerate(["<20%", "20-40%", "40-60%", "60-80%", ">=80%"]):
    print(f"\nPortfolios for {q} quantile:")
    for date, tickers in portfolios[i].items():
        print(f"{date}: {tickers}")


def extend_portfolios_to_months(portfolios):
    
    extended_portfolios = {key: {} for key in range(5)}

    
    start_year = 2013
    end_year = 2022
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            current_date = datetime(year, month, 1)
            month_year = current_date.strftime('%Y-%m')
            
            if month in [1, 2, 3]:
                quarter_month = 10  
                quarter_year = year - 1
            elif month in [4, 5, 6]:
                quarter_month = 1  
                quarter_year = year
            elif month in [7, 8, 9]:
                quarter_month = 4  
                quarter_year = year
            else:  
                quarter_month = 7  
                quarter_year = year

            previous_month_year = datetime(quarter_year, quarter_month, 1).strftime('%Y-%m')

            
            for i in range(5):
                extended_portfolios[i][month_year] = portfolios[i].get(previous_month_year, [])

    return extended_portfolios



extended_portfolios = extend_portfolios_to_months(portfolios)


for i, q in enumerate(["<20%", "20-40%", "40-60%", "60-80%", ">=80%"]):
    print(f"\nExtended portfolios for {q} quantile:")
    for month_year, tickers in sorted(extended_portfolios[i].items()):
        print(f"{month_year}: {tickers}")


def create_returns_portfolio(portfolios, file_name):
    
    with pd.ExcelFile(file_name) as xls:
        sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

    
    returns_portfolios = {key: {} for key in range(5)}

    
    for quantile_index, dates_tickers in portfolios.items():
        for date, tickers in dates_tickers.items():
            returns = []
            for ticker in tickers:
                
                ticker_data = sheets_dict.get(ticker)
                if ticker_data is not None:
                    
                    month_data = ticker_data[ticker_data['year_month'] == date]
                    if not month_data.empty:

                        cur_cup = 0
                        for t in tickers:
                            cur_ticker_data = sheets_dict.get(ticker)
                            cur_month_data = cur_ticker_data[ticker_data['year_month'] == date]
                            cap = cur_month_data['capitalization'].iloc[
                                0] if 'capitalization' in cur_month_data.columns else 0
                            cur_cup += cap

                        cap = month_data['capitalization'].iloc[0] if 'capitalization' in month_data.columns else 0
                        weight = cap / cur_cup if cur_cup else 0  

                        
                        return_rate = (
                                month_data['exchange_rate_frac'].fillna(0) + month_data['div_rate'].fillna(0)).sum()
                        returns.append(weight * return_rate)
                    else:
                        returns.append(0)
                else:
                    returns.append(0)
            returns_portfolios[quantile_index][date] = sum(returns)

    return returns_portfolios


file_name = '../data/filtered_blue_chips (2).xlsx'
returns_portfolios = create_returns_portfolio(extended_portfolios, file_name)


for i, q in enumerate(["<20%", "20-40%", "40-60%", "60-80%", ">=80%"]):
    print(f"\nReturns for {q} quantile:")
    values = returns_portfolios[i].values()  
    mean = sum(values) / len(values)
    print("mean: ", mean * 100)
    for month_year, returns in sorted(returns_portfolios[i].items()):
        print(f"{month_year}: {returns}")
