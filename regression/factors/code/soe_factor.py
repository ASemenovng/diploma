import pandas as pd
import numpy as np
from itertools import product

from result_code.regression.factors.code.smb_factor import market_capa

black_list = {'MERF', 'VRSB', 'ALBK', 'GTLC', 'ZVEZ', 'CHKZ', 'KRKN', 'ROLO', 'TANL', 'PRFN', 'MRSB', 'USBN', 'VJGZ',
              'YAKG', 'KLSB', 'RUSI', 'VGSB', 'NSVZ', 'PRMB', 'MOBB', 'VDSB', 'IRKT', 'NAUK', 'TGKN', 'APTK', 'RGSS',
              'LNZL', 'ODVA', 'MORI', 'LPSB', 'KTSB', 'ISKJ'}


file_name = "../data/upt_upt_filtered_bc.xlsx"
file_name = "../data/filtered_blue_chips-4.xlsx"




with pd.ExcelFile(file_name) as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}










































dates = pd.date_range(start="2012-01-01", end="2022-12-31", freq='MS').strftime('%Y-%m').tolist()

government_owned = {date: [] for date in dates}
non_government_owned = {date: [] for date in dates}


for ticker, df in sheets_dict.items():
    if ticker == 'RGBI':
        continue

    
    df['year_month'] = pd.to_datetime(df['year_month'], format="%Y-%m")
    df['Year'] = df['year_month'].dt.year
    df['Month'] = df['year_month'].dt.month

    
    df['state_property'] = pd.to_numeric(df['state_property'], errors='coerce').fillna(0).astype(int)

    
    for year in range(2012, 2023):
        yearly_data = df[df['Year'] == year]
        if not yearly_data.empty:
            
            first_month_data = yearly_data[yearly_data['Month'] == 1]
            if not first_month_data.empty:
                if first_month_data['state_property'].iloc[0] == 1:
                    relevant_dict = government_owned
                else:
                    relevant_dict = non_government_owned

                
                year_months = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq='MS').strftime(
                    '%Y-%m').tolist()
                for date in year_months:
                    relevant_dict[date].append(ticker)

print("government_owned: ", government_owned)
print("non_government_owned: ", non_government_owned)


government_returns = {date: [] for date in government_owned.keys()}
non_government_returns = {date: [] for date in non_government_owned.keys()}



def calculate_total_return(df, year_month):
    row = df[df['year_month'] == year_month]
    if row.empty or pd.isna(row['div_rate'].iloc[0]):
        exchange_rate_frac = row['exchange_rate_frac'].iloc[0] if not row.empty else 0
        return exchange_rate_frac
    
    
    
    return row['exchange_rate_frac'].iloc[0] / 100 + row['div_rate'].iloc[0]


def calculate_total_returnf(df, year_month, market_capa):
    year = year_month.strftime('%Y')  
    row = df[df['year_month'] == year_month]

    if row.empty:
        return 0  

    cur_cup = 0
    for t in tickers:
        cap = row['capitalization'].iloc[0] if 'capitalization' in row.columns else 0
        cur_cup += cap

    cap = row['capitalization'].iloc[0] if 'capitalization' in row.columns else 0

    weight = cap / cur_cup if cur_cup else 0  
    
    
    
    
    
    
    
    
    

    
    exchange_rate_frac = row['exchange_rate_frac'].iloc[0] if not row.empty and not pd.isna(
        row['exchange_rate_frac'].iloc[0]) else 0
    div_rate = row['div_rate'].iloc[0] if not row.empty and not pd.isna(row['div_rate'].iloc[0]) else 0

    
    return (exchange_rate_frac + div_rate) * weight



for date, tickers in government_owned.items():
    year_month = pd.to_datetime(date)
    for ticker in tickers:
        df = sheets_dict[ticker]
        total_return = calculate_total_return(df, year_month)
        total_return = calculate_total_returnf(df, year_month, market_capa)
        government_returns[date].append(total_return)

for date, tickers in non_government_owned.items():
    year_month = pd.to_datetime(date)
    for ticker in tickers:
        df = sheets_dict[ticker]
        total_return = calculate_total_return(df, year_month)
        total_return = calculate_total_returnf(df, year_month, market_capa)
        non_government_returns[date].append(total_return)

print("government_returns: ", government_returns)
print("non_government_returns: ", non_government_returns)

average_government_returns = {}
average_non_government_returns = {}


for date, returns in government_returns.items():
    if returns:  
        average_return = sum(returns) / len(returns)  
        average_return = sum(returns)
    else:
        average_return = 0  
    average_government_returns[date] = average_return


for date, returns in non_government_returns.items():
    if returns:  
        average_return = sum(returns) / len(returns)  
        average_return = sum(returns)
    else:
        average_return = 0  
    average_non_government_returns[date] = average_return

print("average_government_returns: ", average_government_returns)
print("average_non_government_returns: ", average_non_government_returns)


data = {
    'Date': list(average_government_returns.keys()),
    'Gov Returns': list(average_government_returns.values()),
    'Non-Gov Returns': list(average_non_government_returns.values())
}

df = pd.DataFrame(data)


output_file = '../data/weight_soe_factors_bc.xlsx'
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Returns Summary')


