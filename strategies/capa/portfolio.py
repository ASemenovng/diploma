import pandas as pd
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta


black_list = {'MERF', 'VRSB', 'ALBK', 'GTLC', 'ZVEZ', 'CHKZ', 'KRKN', 'ROLO', 'TANL', 'PRFN', 'MRSB', 'USBN', 'VJGZ',
              'YAKG', 'KLSB', 'RUSI', 'VGSB', 'NSVZ', 'PRMB', 'MOBB', 'VDSB', 'IRKT', 'NAUK', 'TGKN', 'APTK', 'RGSS',
              'LNZL', 'ODVA', 'MORI', 'LPSB', 'KTSB', 'ISKJ'}



file_name = "upt_upt_filtered_bc.xlsx"
file_name = "final_data_for_regression-3.xlsx"




with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}






all_data = pd.concat(sheets_dict.values(), ignore_index=True)
print(all_data.columns)

all_data['year_month'] = pd.to_datetime(all_data['year_month'], format='%Y-%m')


filtered_data = all_data[all_data['year_month'] >= '2013-01-01']


sorted_data = filtered_data.sort_values('year_month')


sorted_data['year_month'] = sorted_data['year_month'].dt.strftime('%Y-%m')

print("sorted_data: ", sorted_data)
all_data = sorted_data



median_values = all_data.groupby('year_month')['capitalization'].median()


median_dict = median_values.to_dict()


print(median_dict)


high_capitalization = defaultdict(list)
low_capitalization = defaultdict(list)


market_capa = {'2012': 19109663295126.965, '2013': 17667291362412.78, '2014': 17123075630215.018, '2015': 18606620134392.96, '2016': 20646611702928.73, '2017': 29854452046976.023, '2018': 30384861570330.758, '2019': 33313651339247.312, '2020': 41427147516278.04, '2021': 45297827049523.67, '2022': 49773691806721.07}




def find_quarter(month):
    if month % 3 == 1:
        return month
    elif month % 3 == 2:
        return month - 1
    else:
        return month - 2


for ticker, df in sheets_dict.items():
    if ticker == 'RGBI' or ticker in black_list:
        continue
    df['year'] = df['year_month'].str.slice(0, 4).astype(int)
    df['month'] = df['year_month'].str.slice(5, 7).astype(int)
    df['quarter_month'] = df['month'].apply(find_quarter)
    df['year_quarter'] = df['year'].astype(str) + '-' + df['quarter_month'].astype(str).str.zfill(2)

   
    for index, row in df.iterrows():
        year_month = row['year_quarter']
        if year_month < '2013-01-01':
            continue
        if row['capitalization'] >= median_dict.get(row['year_month'], 0):
            high_capitalization[year_month].append(ticker)
        else:
            low_capitalization[year_month].append(ticker)


high_capitalization = dict(high_capitalization)
low_capitalization = dict(low_capitalization)











for date in high_capitalization:
    high_capitalization[date] = list(set(high_capitalization[date]))

for date in low_capitalization:
    low_capitalization[date] = list(set(low_capitalization[date]))


print("Портфель с капитализацией выше или равной медианной (уникальные тикеры):")
for date, tickers in high_capitalization.items():
    print(f"{date}: {tickers}")

print("\nПортфель с капитализацией ниже медианной (уникальные тикеры):")
for date, tickers in low_capitalization.items():
    print(f"{date}: {tickers}")


def fill_missing_quarter_months(cap_dict):
    new_dict = {}
    months_to_add = [1, 2, 3] 

    for date in sorted(cap_dict):
        year, month = map(int, date.split('-'))
        quarter_start_month = 1 + 3 * ((month - 1) // 3)
        for m in months_to_add:
            new_month = quarter_start_month + (m - 1)
            new_date = f"{year}-{new_month:02d}"
            if new_month < month:
                if new_date not in new_dict: 
                    continue
            elif new_month == month:
                new_dict[new_date] = cap_dict[date]
            else:
                if new_month < 13: 
                    new_dict[new_date] = cap_dict[date]

    return new_dict



high_capitalization = fill_missing_quarter_months(high_capitalization)
low_capitalization = fill_missing_quarter_months(low_capitalization)


print("Расширенный high_capitalization:")
for date in sorted(high_capitalization):
    print(f"{date}: {high_capitalization[date]}")

print("\nРасширенный low_capitalization:")
for date in sorted(low_capitalization):
    print(f"{date}: {low_capitalization[date]}")


def create_weighted_returns_dict_portolios(capitalization_dict, sheets_dict):
    returns_dict = defaultdict(list)
    for date, tickers in capitalization_dict.items():
        returns = 0
        for ticker in tickers:
            df = sheets_dict[ticker]
            specific_row = df[df['year_month'] == date]
            if not specific_row.empty:
                cap = specific_row['capitalization'].iloc[
                    0] if 'capitalization' in specific_row.columns else 0
                returns += cap
        returns_dict[date] = returns
    return returns_dict


def create_weighted_returns_dict(capitalization_dict, sorted_market_capitalization, sheets_dict):
    returns_dict = defaultdict(list)
    for date, tickers in capitalization_dict.items():
        for ticker in tickers:
            if ticker in sheets_dict:
                df = sheets_dict[ticker]
                specific_row = df[df['year_month'] == date]

                if not specific_row.empty:
                    cur_cup = sorted_market_capitalization[date]
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   

                    cap = specific_row['capitalization'].iloc[0] if 'capitalization' in specific_row.columns else 0
                    exchange_rate_frac = specific_row['exchange_rate_frac'].iloc[
                        0] if 'exchange_rate_frac' in specific_row.columns else 0
                    div_rate = specific_row['div_rate'].iloc[0] if 'div_rate' in specific_row.columns and not pd.isna(
                        specific_row['div_rate'].iloc[0]) else 0

                    weight = cap / cur_cup if cur_cup else 0 
                   
                   
                   
                    weighted_exchange = exchange_rate_frac * weight
                    weighted_div = div_rate * weight
                    returns_dict[date].append((weighted_exchange, weighted_div))

    return dict(returns_dict)

































high_market_returns = create_weighted_returns_dict_portolios(high_capitalization, sheets_dict)
low_market_capitalization = create_weighted_returns_dict_portolios(low_capitalization, sheets_dict)
print("high_total_returns: ", high_market_returns)
print("low_total_capitalization: ", low_market_capitalization)




high_returns = create_weighted_returns_dict(high_capitalization, high_market_returns, sheets_dict)
low_returns = create_weighted_returns_dict(low_capitalization, low_market_capitalization, sheets_dict)




print("Доходности для портфеля с капитализацией выше или равной медианной:")
for date, returns in high_returns.items():
    print(f"{date}: {returns}")

print("\nДоходности для портфеля с капитализацией ниже медианной:")
for date, returns in low_returns.items():
    print(f"{date}: {returns}")




def average_tuples(tuples_list):
    if not tuples_list:
        return 0, 0 

   
    exchange_rates = [tup[0] for tup in tuples_list if tup[0] is not None]
    div_yields = [tup[1] if tup[1] is not None and not pd.isna(tup[1]) else 0 for tup in tuples_list] 

    print("exchange_rates: ", exchange_rates)
   
    avg_exchange_rate = sum(exchange_rates) * 100 if exchange_rates else 0
   
   
   
    avg_div_yield = sum(div_yields) * 100 if div_yields else 0
    avg_div_yield = sum(
        0 if pd.isna(yield_value) else yield_value for yield_value in div_yields) * 100 if div_yields else 0

   

    print("avg_exchange_rate, avg_div_yield: ", avg_exchange_rate, avg_div_yield)

    return avg_exchange_rate, avg_div_yield



high_returns_avg = {date: average_tuples(tuples) for date, tuples in high_returns.items()}
low_returns_avg = {date: average_tuples(tuples) for date, tuples in low_returns.items()}



print("high_returns_avg:")
for date, value in high_returns_avg.items():
    print(f"{date}: {value}")

print("\nlow_returns_avg:")
for date, value in low_returns_avg.items():
    print(f"{date}: {value}")



def plot_portfolio_returns(portfolio, portfolio_name):
   
    dates = list(portfolio.keys())
    dates = pd.to_datetime(dates)
    exchange_rates = [max(0, p[0]) for p in portfolio.values()] 
    exchange_rates_neg = [min(0, p[0]) for p in portfolio.values()] 
    div_rates = [p[1] for p in portfolio.values()]

   
    plt.figure(figsize=(12, 6))
    plt.bar(dates, exchange_rates, width=25, color='blue', label='Курсовая доходность')
    plt.bar(dates, exchange_rates_neg, width=25, color='cyan', label='Курсовая доходность (отрицательная)')
    plt.bar(dates, div_rates, bottom=exchange_rates, width=25, color='green', label='Дивидендная доходность')

   
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)

   
    plt.title(f'Доходность портфеля {portfolio_name}')
    plt.xlabel('Дата')
    plt.ylabel('Доходность')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()



plot_portfolio_returns(high_returns_avg, "акций, капитализация которых выше медианы")
plot_portfolio_returns(low_returns_avg, "акций, капитализация которых ниже медианы")



def sum_tuple(tuple):
    if not tuple:
        return 0 

   
    exchange_rates = tuple[0] if tuple[0] else 0
    div_yields = tuple[1] if not pd.isna(tuple[1]) else 0

    print("exchange_rates: ", exchange_rates, " div_yields: ", div_yields, " pd.isna: ", pd.isna(div_yields), " is None: ", div_yields is None)

    return exchange_rates, div_yields


high_returns_avg = {date: sum_tuple(tuple) for date, tuple in high_returns_avg.items()}
low_returns_avg = {date: sum_tuple(tuple) for date, tuple in low_returns_avg.items()}

print("high_returns_avg: ", high_returns_avg)
print("low_returns_avg: ", low_returns_avg)


def honest_sum_tuple(tuple):
    if not tuple:
        return 0 

   
    exchange_rates = tuple[0] if tuple[0] else 0
    div_yields = tuple[1] if not pd.isna(tuple[1]) else 0

   
    return exchange_rates + div_yields



h_high_returns_avg = {date: honest_sum_tuple(tuple) for date, tuple in high_returns_avg.items()}
h_low_returns_avg = {date: honest_sum_tuple(tuple) for date, tuple in low_returns_avg.items()}






df = pd.read_excel("stat_test_for_portfolios_new.xlsx")
print("h_high_returns_avg: ", h_high_returns_avg)
df['high capa'] = list(h_high_returns_avg.values())

df['low capa'] = list(h_low_returns_avg.values())



output_filename = "stat_test_for_portfolios_new.xlsx"



print("df")
df = df.to_string(max_colwidth=None)
print(df)













def plot_portfolio_returns_with_moving_average(portfolio, portfolio_name):
   
    dates = pd.to_datetime(list(portfolio.keys()))
    values = list(portfolio.values())

   
    df = pd.DataFrame({'Date': dates, 'Value': values})

   
    df.set_index('Date', inplace=True)
    df['MA'] = df['Value'].rolling(window=6, min_periods=1).mean()

   
    plt.figure(figsize=(12, 6))
    plt.bar(df.index, df['Value'], width=25, color='blue', label=f'Доходность {portfolio_name}')
    plt.plot(df.index, df['MA'], color='red', linestyle='-', linewidth=1, label='Скользящее среднее 6 месяцев')

   
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)

   
    plt.title(f'Доходность портфеля {portfolio_name}')
    plt.xlabel('Дата')
    plt.ylabel('Доходность')
    plt.legend()
    plt.grid(True)
    plt.show()










def calculate_cumulative_returns(monthly_returns):
    cumulative_returns = {}
    cumulative_product = 1
    for date, return_value in monthly_returns.items():
        cumulative_product *= (return_value / 100 + 1)
        cumulative_returns[date] = (cumulative_product - 1) * 100
    return cumulative_returns


def calculate_cumulative_returns_separatly(monthly_returns):
    cumulative_returns = {}
    cumulative_product = 1
    for date, tuple_return in monthly_returns.items():
        cumulative_product *= (tuple_return[0] / 100 + 1)
        cumulative_product += (tuple_return[1] / 100)
        cumulative_returns[date] = (cumulative_product - 1) * 100
    return cumulative_returns


def plot_portfolio_returns(with_rolling_average, portfolio_name):
   
    dates = pd.to_datetime(list(with_rolling_average.keys()))
    values = list(with_rolling_average.values())

    df = pd.DataFrame({'Date': dates, 'Value': values})
    df.set_index('Date', inplace=True)

   
    df['MA'] = df['Value'].rolling(window=6, min_periods=1).mean()

   
    plt.figure(figsize=(12, 6))
    plt.bar(df.index, df['Value'], width=25, color='blue', label=f'Доходность {portfolio_name}')
    plt.plot(df.index, df['MA'], color='red', linestyle='-', linewidth=1, label='Скользящее среднее 6 месяцев')

   
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45)

    plt.title(f'Накопленная доходность портфеля {portfolio_name}')
    plt.xlabel('Дата')
    plt.ylabel('Накопленная доходность (%)')
    plt.legend()
    plt.grid(True)
    plt.show()







cum_high_returns_avg = calculate_cumulative_returns_separatly(high_returns_avg)
cum_low_returns_avg = calculate_cumulative_returns_separatly(low_returns_avg)

print("cum_high_returns_avg: ", cum_high_returns_avg)
print("cum_low_returns_avg: ", cum_low_returns_avg)


plot_portfolio_returns(cum_high_returns_avg, "акций, капитализация которых выше медианы")
plot_portfolio_returns(cum_low_returns_avg, "акций, капитализация которых ниже медианы")
