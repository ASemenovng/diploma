import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



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



sheets_dict.pop('MERF')
sheets_dict.pop('VRSB')
sheets_dict.pop('ALBK')
sheets_dict.pop('GTLC')
sheets_dict.pop('ZVEZ')
sheets_dict.pop('CHKZ')
sheets_dict.pop('KRKN')
sheets_dict.pop('ROLO')


sheets_dict.pop('TANL')
sheets_dict.pop('PRFN')
sheets_dict.pop('MRSB')
sheets_dict.pop('USBN')
sheets_dict.pop('VJGZ')


sheets_dict.pop('YAKG')
sheets_dict.pop('KLSB')
sheets_dict.pop('RUSI')
sheets_dict.pop('VGSB')
sheets_dict.pop('NSVZ')
sheets_dict.pop('PRMB')
sheets_dict.pop('MOBB')
sheets_dict.pop('VDSB')
sheets_dict.pop('IRKT')
sheets_dict.pop('NAUK')
sheets_dict.pop('TGKN')
sheets_dict.pop('APTK')
sheets_dict.pop('RGSS')
sheets_dict.pop('LNZL')
sheets_dict.pop('ODVA')
sheets_dict.pop('MORI')
sheets_dict.pop('LPSB')
sheets_dict.pop('KTSB')
sheets_dict.pop('ISKJ')





for sheet_name, df in sheets_dict.items():
    if sheet_name == 'RGBI':
        continue

    df['year_month'] = pd.to_datetime(df['year_month']).dt.strftime('%Y-%m')

   
    for date in no_dividend_portfolio.keys():
        year_month_target = pd.Timestamp(date)

       
        monthly_data = df[df['year_month'] == date]

        if not monthly_data.empty:
            exchange_rate = monthly_data['exchange_rate_frac'].values[0]
            if exchange_rate > 1 or exchange_rate < -1:
                print("sheet_name: ", sheet_name, " for date: ", date, " with exchange_rate: ", exchange_rate)
                if sheet_name in no_dividend_portfolio[date]:
                    print("no_dividend_portfolio\n")
                if sheet_name in below_median_portfolio[date]:
                    print("below_median_portfolio\n")
                if sheet_name in above_median_portfolio[date]:
                    print("above_median_portfolio\n")

            div_rate = monthly_data['div_rate'].values[0]

           
            if sheet_name in no_dividend_portfolio[date]:
                no_dividend_portfolio_tuples[date].append((exchange_rate, div_rate))

           
            if sheet_name in below_median_portfolio[date]:
                below_median_portfolio_tuples[date].append((exchange_rate, div_rate))

           
            if sheet_name in above_median_portfolio[date]:
                above_median_portfolio_tuples[date].append((exchange_rate, div_rate))


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
    div_yields = [tup[1] if tup[1] is not None else 0 for tup in tuples_list] 

   
    avg_exchange_rate = np.mean(exchange_rates) * 100 if exchange_rates else 0
    avg_div_yield = np.mean(div_yields) * 100 if div_yields else 0

    return avg_exchange_rate, avg_div_yield



no_dividend_avg = {date: average_tuples(tuples) for date, tuples in no_dividend_portfolio_tuples.items()}
below_median_avg = {date: average_tuples(tuples) for date, tuples in below_median_portfolio_tuples.items()}
above_median_avg = {date: average_tuples(tuples) for date, tuples in above_median_portfolio_tuples.items()}


print("No 1 Dividend Portfolio Average by Month and Year:")
for date, value in no_dividend_avg.items():
    print(f"{date}: {value}")

print("\nBelow 1 Median Dividend Portfolio Average by Month and Year:")
for date, value in below_median_avg.items():
    print(f"{date}: {value}")

print("\nAbove 1 Median Dividend Portfolio Average by Month and Year:")
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


def calculate_cumulative_returns(monthly_returns):
    cumulative_returns = {}
    cumulative_product = 1
    for date, return_value in monthly_returns.items():
        cumulative_product *= (return_value / 100 + 1)
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


above_median_avg['2014-03'] = 1


cum_no_dividend_avg = calculate_cumulative_returns(no_dividend_avg)
cum_below_median_avg = calculate_cumulative_returns(below_median_avg)
cum_above_median_avg = calculate_cumulative_returns(above_median_avg)


plot_portfolio_returns(cum_no_dividend_avg, "Без Дивидендов")
plot_portfolio_returns(cum_below_median_avg, "Ниже медианы")
plot_portfolio_returns(cum_above_median_avg, "Выше медианы")
