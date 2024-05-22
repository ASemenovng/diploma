import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



file_name = "../data/filtered_blue_chips.xlsx"
file_name = "../data/final_data_for_regression-3.xlsx"


with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


all_data = pd.concat(sheets_dict.values(), ignore_index=True)


grouped_data = all_data.groupby('year_month')



def calculate_median(series):
    if series.dropna().empty:
        return 0 
    else:
        return series.median()



median_values = grouped_data['div_rate'].apply(calculate_median)


median_dict = median_values.to_dict()


print(median_dict)









no_dividend_portfolio = {f"{year}-{month:02d}": [] for year in range(2013, 2023) for month in range(1, 13)}
below_median_portfolio = {f"{year}-{month:02d}": [] for year in range(2013, 2023) for month in range(1, 13)}
above_median_portfolio = {f"{year}-{month:02d}": [] for year in range(2013, 2023) for month in range(1, 13)}


for sheet_name, df in sheets_dict.items():
    if sheet_name == 'RGBI':
        continue

   
    df['year_month'] = pd.to_datetime(df['year_month'])
    df = df[(df['year_month'] >= '2011-01') & (df['year_month'] <= '2022-12')]

    for year in range(2013, 2023):
       
        first_month_data = df[df['year_month'] == f"{year-1}-01-01"]
        if not first_month_data.empty:
            ticker = first_month_data['ticker'].values[0]
            div_rate = first_month_data['div_rate'].values[0]
            median_value = median_dict.get(f"{year-1}-01")

           
            if pd.isna(div_rate) or div_rate == 0:
                portfolio = no_dividend_portfolio
            elif div_rate < median_value:
                portfolio = below_median_portfolio
            else:
                portfolio = above_median_portfolio

           
            for month in range(1, 13):
                portfolio[f"{year}-{month:02d}"].append(ticker)


print("No Dividend Portfolio by Month and Year:")
for date, value in no_dividend_portfolio.items():
    print(f"{date}: {value}")

print("\nBelow Median Dividend Portfolio by Month and Year:")
for date, value in below_median_portfolio.items():
    print(f"{date}: {value}")

print("\nAbove Median Dividend Portfolio by Month and Year:")
for date, value in above_median_portfolio.items():
    print(f"{date}: {value}")

















































no_dividend_portfolio_tuples = {date: [] for date in no_dividend_portfolio.keys()}
below_median_portfolio_tuples = {date: [] for date in below_median_portfolio.keys()}
above_median_portfolio_tuples = {date: [] for date in above_median_portfolio.keys()}


for sheet_name, df in sheets_dict.items():
    if sheet_name == 'RGBI':
        continue

    df['year_month'] = pd.to_datetime(df['year_month']).dt.strftime('%Y-%m')

   
    for date in no_dividend_portfolio.keys():
        year_month_target = pd.Timestamp(date)

       
        monthly_data = df[df['year_month'] == date]

        if not monthly_data.empty:
            exchange_rate = monthly_data['exchange_rate_frac'].values[0]
           
           

            div_rate = monthly_data['div_rate'].values[0]

           
            if sheet_name in no_dividend_portfolio[date]:

                cur_cup = 0
                for t in no_dividend_portfolio[date]:
                    if not monthly_data.empty:
                        cap = monthly_data['capitalization'].iloc[0] if 'capitalization' in monthly_data.columns else 0
                        cur_cup += cap
                cap = monthly_data['capitalization'].iloc[0] if 'capitalization' in monthly_data.columns else 0
                weight = cap / cur_cup if cur_cup else 0 
               
                weighted_exchange = exchange_rate * weight
                weighted_div = div_rate * weight

                no_dividend_portfolio_tuples[date].append((weighted_exchange, weighted_div))
               

           
            if sheet_name in below_median_portfolio[date]:

                cur_cup = 0
                for t in below_median_portfolio[date]:
                    if not monthly_data.empty:
                        cap = monthly_data['capitalization'].iloc[0] if 'capitalization' in monthly_data.columns else 0
                        cur_cup += cap
                cap = monthly_data['capitalization'].iloc[0] if 'capitalization' in monthly_data.columns else 0
                weight = cap / cur_cup if cur_cup else 0 
               
                weighted_exchange = exchange_rate * weight
                weighted_div = div_rate * weight

                below_median_portfolio_tuples[date].append((weighted_exchange, weighted_div))

               

           
            if sheet_name in above_median_portfolio[date]:

                cur_cup = 0
                for t in above_median_portfolio[date]:
                    if not monthly_data.empty:
                        cp = monthly_data['capitalization'].iloc[0] if 'capitalization' in monthly_data.columns else 0
                        cur_cup += cp
                cap = monthly_data['capitalization'].iloc[0] if 'capitalization' in monthly_data.columns else 0
                weight = cap / cur_cup if cur_cup else 0 
                if sheet_name == 'RTKM':
                    print("weight: ", weight, " cap: ", cap, " cur_cup: ", cur_cup, " for date: ", date)
               
                weighted_exchange = exchange_rate * weight
                weighted_div = div_rate * weight

                above_median_portfolio_tuples[date].append((weighted_exchange, weighted_div))
               


print("No Dividend Portfolio by Month and Year:")
for date, value in no_dividend_portfolio_tuples.items():
    print(f"{date}: {value}")

print("\nBelow Median Dividend Portfolio by Month and Year:")
for date, value in below_median_portfolio_tuples.items():
    print(f"{date}: {value}")

print("\nAbove Median Dividend Portfolio by Month and Year:")
for date, value in above_median_portfolio_tuples.items():
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



no_dividend_avg = {date: average_tuples(tuples) for date, tuples in no_dividend_portfolio_tuples.items()}
below_median_avg = {date: average_tuples(tuples) for date, tuples in below_median_portfolio_tuples.items()}
above_median_avg = {date: average_tuples(tuples) for date, tuples in above_median_portfolio_tuples.items()}


print("No Dividend Portfolio Average by Month and Year:")
for date, value in no_dividend_avg.items():
    print(f"{date}: {value}")

print("\nBelow Median Dividend Portfolio Average by Month and Year:")
for date, value in below_median_avg.items():
    print(f"{date}: {value}")

print("\nAbove Median Dividend Portfolio Average by Month and Year:")
for date, value in above_median_avg.items():
    print(f"{date}: {value}")


def sum_tuple(tuple):
    if not tuple:
        return 0 

   
    exchange_rates = tuple[0] if tuple[0] else 0
    div_yields = tuple[1] if not pd.isna(tuple[1]) else 0

    print("exchange_rates: ", exchange_rates, " div_yields: ", div_yields, " pd.isna: ", pd.isna(div_yields), " is None: ", div_yields is None)

    return exchange_rates + div_yields

   
   
   
   


no_dividend_avg = {date: sum_tuple(tuple) for date, tuple in no_dividend_avg.items()}
below_median_avg = {date: sum_tuple(tuple) for date, tuple in below_median_avg.items()}
above_median_avg = {date: sum_tuple(tuple) for date, tuple in above_median_avg.items()}


print("No Dividend Portfolio Average by Month and Year:")
for date, value in no_dividend_avg.items():
    print(f"{date}: {value}")

print("\nBelow Median Dividend Portfolio Average by Month and Year:")
for date, value in below_median_avg.items():
    print(f"{date}: {value}")

print("\nAbove Median Dividend Portfolio Average by Month and Year:")
for date, value in above_median_avg.items():
    print(f"{date}: {value}")





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



plot_portfolio_returns_with_moving_average(no_dividend_avg, "Без Дивидендов")
plot_portfolio_returns_with_moving_average(below_median_avg, "Ниже Медианы")
plot_portfolio_returns_with_moving_average(above_median_avg, "Выше Медианы")






initial_value = 100


def returns_to_prices(returns):
    prices = [initial_value]
    for r in returns:
        prices.append(prices[-1] * (1 + r / 100))
    return prices[1:] 



trimmed_no_dividend_avg = returns_to_prices(list(no_dividend_avg.values()))[11:]
trimmed_below_median_avg = returns_to_prices(list(below_median_avg.values()))[11:]
trimmed_above_median_avg = returns_to_prices(list(above_median_avg.values()))[11:]


data = {
    'Date': pd.to_datetime(list(no_dividend_avg.keys())[11:]),
    'no_dividend_avg': trimmed_no_dividend_avg,
    'below_median_avg': trimmed_below_median_avg,
    'above_median_avg': trimmed_above_median_avg
   
   
   
}

df = pd.DataFrame(data)
df.set_index('Date', inplace=True)


df_returns = df.pct_change()


volatility = df_returns.std()

print("Стандартные отклонения возвратов для каждого портфеля после учета абсолютных значений:")
print(volatility)

























most_volatile = volatility.idxmax()

print(f"Наиболее волатильный портфель: {most_volatile} с волатильностью {volatility[most_volatile]}")








new_file_path = '../data/Факторы итог new-2.xlsx'
save_file_path = '../data/portfolios_for_reg.xlsx'


new_df = pd.read_excel(new_file_path)


new_df['date'] = pd.to_datetime(new_df['date'])
filtered_new_df = new_df[new_df['date'] >= pd.to_datetime('2013-01')]


data = {
    'date': pd.to_datetime(list(no_dividend_avg.keys())),
    'no_dividend_avg': [x / 100 for x in list(no_dividend_avg.values())],
    'below_median_avg': [x / 100 for x in list(below_median_avg.values())],
    'above_median_avg': [x / 100 for x in list(above_median_avg.values())]
}
df = pd.DataFrame(data)


filtered_df = df[df['date'] >= pd.to_datetime('2013-01')]


combined_df = pd.merge(filtered_df, filtered_new_df, on='date', how='outer')


combined_df.sort_values(by='date', inplace=True)


combined_df.reset_index(drop=True, inplace=True)


combined_df.to_excel(save_file_path, index=False)

print(f"Данные сохранены в файл: {save_file_path}")







data = {
    'Date': pd.to_datetime(list(no_dividend_avg.keys())),
    'no_dividend_avg': list(no_dividend_avg.values()),
    'below_median_avg': list(below_median_avg.values()),
    'above_median_avg': list(above_median_avg.values())
}
df = pd.DataFrame(data)

df.set_index('Date', inplace=True)


start_date = '2013-01'
filtered_df = df[df.index >= pd.to_datetime(start_date)]


filtered_df.reset_index(inplace=True)


file_path = '../data/filtered_portfolios.xlsx'
filtered_df.to_excel(file_path, index=False)

print(f"Данные сохранены в файл: {file_path}")
