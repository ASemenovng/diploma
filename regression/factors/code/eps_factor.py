import pandas as pd
from collections import defaultdict
import statistics

black_list = {'MERF', 'VRSB', 'ALBK', 'GTLC', 'ZVEZ', 'CHKZ', 'KRKN', 'ROLO', 'TANL', 'PRFN', 'MRSB', 'USBN', 'VJGZ',
              'YAKG', 'KLSB', 'RUSI', 'VGSB', 'NSVZ', 'PRMB', 'MOBB', 'VDSB', 'IRKT', 'NAUK', 'TGKN', 'APTK', 'RGSS',
              'LNZL', 'ODVA', 'MORI', 'LPSB', 'KTSB', 'ISKJ'}



file_name = "../data/upt_upt_filtered_bc.xlsx"



with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}















































all_payouts = []

for ticker, df in sheets_dict.items():
    if ticker == 'RGBI':
        continue
    
    df_dec = df[df['year_month'].str.endswith('12')]
    
    df_valid = df_dec[df_dec['eps'].notna()]
    all_payouts.append(df_valid[['year_month', 'eps']])


all_payout_data = pd.concat(all_payouts, ignore_index=True)


median_payout_per_year = all_payout_data.groupby('year_month')['eps'].median()


median_payout_dict = median_payout_per_year.to_dict()


print("Медианные значения eps за каждый декабрь:")
for date, median_value in median_payout_dict.items():
    print(f"{date}: {median_value}")




high_div_portfolio = {f"{year}-{month:02d}": [] for year in range(2012, 2023) for month in range(1, 13)}
low_div_portfolio = {f"{year}-{month:02d}": [] for year in range(2012, 2023) for month in range(1, 13)}


for ticker, df in sheets_dict.items():
    if ticker == 'RGBI':
        continue
    for year in range(2012, 2023):
        december_key = f"{year}-12"

        
        december_data = df[df['year_month'] == december_key]

        if not december_data.empty and pd.notna(december_data['dividend_payout_RUB'].values[0]):
            median_value = median_payout_dict.get(december_key)
            eps = december_data['eps'].values[0]

            if pd.notna(eps):
                
                for month in range(1, 13):
                    if median_value is not None:
                        if eps >= median_value:
                            high_div_portfolio[f"{year}-{month:02d}"].append(ticker)
                        else:
                            low_div_portfolio[f"{year}-{month:02d}"].append(ticker)
                    else:
                        
                        high_div_portfolio[f"{year}-{month:02d}"].append(ticker)


print("High eps portfolio:")
for key, value in sorted(high_div_portfolio.items()):
    print(f"{key}: {value}")

print("\nLow eps portfolio:")
for key, value in sorted(low_div_portfolio.items()):
    print(f"{key}: {value}")






high_div_returns = {}
low_div_returns = {}


def create_returns_dict(capitalization_dict):
    returns_dict = defaultdict(list)
    for date, tickers in capitalization_dict.items():
        if len(tickers) == 0:
            returns_dict[date].append(0)
        for ticker in tickers:
            if ticker in sheets_dict:
                df = sheets_dict[ticker]
                specific_row = df[df['year_month'] == date]
                if not specific_row.empty:
                    exchange_rate_frac = specific_row['exchange_rate_frac'].iloc[0] if 'exchange_rate_frac' in specific_row.columns else 0
                    div_rate = specific_row['div_rate'].iloc[0] if 'div_rate' in specific_row.columns and not pd.isna(specific_row['div_rate'].iloc[0]) else 0
                    returns_dict[date].append(exchange_rate_frac + div_rate)
    return dict(returns_dict)


high_returns = create_returns_dict(high_div_portfolio)
low_returns = create_returns_dict(low_div_portfolio)


print("Доходности для портфеля с eps выше или равной медианной:")
for date, returns in high_returns.items():
    print(f"{date}: {returns}")

print("\nДоходности для портфеля с eps ниже медианной:")
for date, returns in low_returns.items():
    print(f"{date}: {returns}")






def calculate_average_returns(returns_dict):
    average_returns = {}
    for date, returns in returns_dict.items():
        if returns:  
            average_returns[date] = statistics.mean(returns)
        else:
            average_returns[date] = 0  
    return average_returns


average_high_returns = calculate_average_returns(high_returns)
average_low_returns = calculate_average_returns(low_returns)


print("Средняя доходность для портфеля с eps выше или равной медианной:")
for date, avg_return in average_high_returns.items():
    print(f"{date}: {avg_return:.2f}")

print("\nСредняя доходность для портфеля с eps ниже медианной:")
for date, avg_return in average_low_returns.items():
    print(f"{date}: {avg_return:.2f}")






data = {
    'Date': list(average_high_returns.keys()),
    'High eps Returns': list(average_high_returns.values()),
    'Low eps Returns': [average_low_returns[date] for date in average_high_returns.keys()]  
}

df = pd.DataFrame(data)


output_filename = "../data/eps_factors_bc.xlsx"
df.to_excel(output_filename, index=False, sheet_name='Returns Summary')

print(f"Данные успешно сохранены в файл {output_filename}")
