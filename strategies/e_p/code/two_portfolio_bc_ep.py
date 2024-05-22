import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime



file_name = "../data/filtered_blue_chips_with_ep.xlsx"
file_name = "../data/all_data_with_ep.xlsx"


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

final_medians = {2012: 0.0927343941782047, 2013: 0.08746678646783736, 2014: 0.06809013565667602, 2015: 0.07829107371080113, 2016: 0.08470722336794635, 2017: 0.05395670657446295, 2018: 0.05167082554120872, 2019: 0.09202766631031509, 2020: 0.07473287150854784, 2021: 0.0895812096886025, 2022: 0.1110617829017947}





portfolio_1 = {}
portfolio_2 = {}


for year in range(2013, 2023):
    date_key = f'{year}-12'
    portfolio_1[date_key] = []
    portfolio_2[date_key] = []


for ticker, df in sheets_dict.items():
    if ticker == 'RGBI':
        continue

   
    df['year'] = pd.to_datetime(df['year_month']).dt.year
    df['month'] = pd.to_datetime(df['year_month']).dt.month

    prev_year_payout = None 
   
    for year in range(2012, 2023):
        current_data = df[(df['year'] == year) & (df['month'] == 12)]
        if not current_data.empty:
            current_payout = current_data.iloc[0]['e/p']
            if year >= 2013: 
                if prev_year_payout is None or pd.isna(prev_year_payout) or prev_year_payout < final_medians[year - 1]:
                    portfolio_1[f'{year}-12'].append(ticker)
                else:
                    portfolio_2[f'{year}-12'].append(ticker)
            prev_year_payout = current_payout 




for year in range(2013, 2023):
    date_key = f'{year}-12'
   
    for m in range(1, 12):
        if m <= 9:
            new_key = f'{year}-0{m}'
        else:
            new_key = f'{year}-{m}'
       
       
       
        portfolio_1[new_key] = portfolio_1[date_key]
        portfolio_2[new_key] = portfolio_2[date_key]





def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m')


sorted_portfolio_1_keys = sorted(portfolio_1, key=parse_date)
sorted_portfolio_2_keys = sorted(portfolio_2, key=parse_date)


portfolio_1 = {date: portfolio_1[date] for date in sorted_portfolio_1_keys}
portfolio_2 = {date: portfolio_2[date] for date in sorted_portfolio_2_keys}




print("\nПортфель 1:")
for date, value in portfolio_1.items():
    print("type: ", type(date))
    print(f"{date}: {value}")

print("Портфель 2:")
for date, value in portfolio_2.items():
    print(f"{date}: {value}")













portfolio_1_tuples = {date: [] for date in portfolio_1.keys()}
portfolio_2_tuples = {date: [] for date in portfolio_2.keys()}



for sheet_name, df in sheets_dict.items():
    if sheet_name == 'RGBI':
        continue

    df['year_month'] = pd.to_datetime(df['year_month']).dt.strftime('%Y-%m')

   
    for date in portfolio_1.keys():

       
        monthly_data = df[df['year_month'] == date]

        if not monthly_data.empty:
           
            exchange_rate = monthly_data['exchange_rate'].values[0] / 100
            if sheet_name == 'IRAO':
                exchange_rate = 0.1

            if exchange_rate > 1 or exchange_rate < -1:
                print("sheet_name: ", sheet_name, " for date: ", date, " with exchange_rate: ", exchange_rate)

            div_rate = monthly_data['div_rate'].values[0]

           
           
           

           
            if sheet_name in portfolio_1[date]:

                cur_cup = 0
                for t in portfolio_1[date]:
                    if not monthly_data.empty:
                        cap = monthly_data['capitalization'].iloc[
                            0] if 'capitalization' in monthly_data.columns else 0
                        cur_cup += cap
                cap = monthly_data['capitalization'].iloc[0] if 'capitalization' in monthly_data.columns else 0
                weight = cap / cur_cup if cur_cup else 0 
               
                weighted_exchange = exchange_rate * weight
                weighted_div = div_rate * weight

               
                portfolio_1_tuples[date].append((weighted_exchange, weighted_div))

           
           
           

           
            if sheet_name in portfolio_2[date]:

                cur_cup = 0
                for t in portfolio_1[date]:
                    if not monthly_data.empty:
                        cap = monthly_data['capitalization'].iloc[0] if 'capitalization' in monthly_data.columns else 0
                        cur_cup += cap
                cap = monthly_data['capitalization'].iloc[0] if 'capitalization' in monthly_data.columns else 0
                weight = cap / cur_cup if cur_cup else 0 
                weighted_exchange = exchange_rate * weight
                weighted_div = div_rate * weight

               
                portfolio_2_tuples[date].append((0.9 * weighted_exchange, 0.9 * weighted_div))



print("test")
print(portfolio_1['2013-01'])
print(portfolio_1_tuples['2013-01'])


print("portfolio_1_tuple:")
for date, value in portfolio_1_tuples.items():
    print(f"{date}: {value}")

print("\nportfolio_2_tuple:")
for date, value in portfolio_2_tuples.items():
    print(f"{date}: {value}")







def average_tuples(tuples_list):
    if not tuples_list:
        return 0, 0 

   
    exchange_rates = [tup[0] for tup in tuples_list if tup[0] is not None]
    div_yields = [tup[1] if tup[1] is not None and not pd.isna(tup[1]) else 0 for tup in tuples_list] 

   
    avg_exchange_rate = np.mean(exchange_rates) * 100 if exchange_rates else 0
    avg_div_yield = np.mean(div_yields) * 100 if div_yields else 0

    avg_exchange_rate = sum(exchange_rates) * 100 if exchange_rates else 0
    avg_div_yield = sum(div_yields) * 100 if div_yields else 0
    return avg_exchange_rate, avg_div_yield



portfolio_1_avg = {date: average_tuples(tuples) for date, tuples in portfolio_1_tuples.items()}
portfolio_2_avg = {date: average_tuples(tuples) for date, tuples in portfolio_2_tuples.items()}



print("portfolio_1_avg:")
for date, value in portfolio_1_avg.items():
    print(f"{date}: {value}")

print("\nportfolio_2_avg:")
for date, value in portfolio_2_avg.items():
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



plot_portfolio_returns(portfolio_1_avg, "акций, показатель E/P которых ниже медианы")
plot_portfolio_returns(portfolio_2_avg, "акций, показатель E/P которых выше медианы")
