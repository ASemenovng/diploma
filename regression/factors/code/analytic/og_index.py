import pandas as pd

with pd.ExcelFile('all_data_with_state.xlsx') as xls:
    sheets_dict = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

companies_data = {}

lst = ['ROSN', 'LKOH', 'GAZP', 'NVTK', 'TATN', 'SNGS', 'BANE', 'TRNF', 'RNFT']

for ticker in lst:
    if ticker in sheets_dict:
        df = sheets_dict[ticker]

        
        net_profit = df[df['year_month'].str[-2:] == '12']['net_profit'].values[0]

        
        state_property = df[df['year_month'].str[-2:] == '12']['state_property'].values[0]

        
        b_m = df[df['year_month'].str[-2:] == '12']['B/M'].values[0]
        

        
        eps = df[df['year_month'].str[-2:] == '12']['eps'].values[0]

        
        e_p = df[df['year_month'].str[-2:] == '12']['e/p'].values[0]

        
        mean_net_profit = df['net_profit'].mean() if df['net_profit'].notnull().any() else None
        mean_state_property = df['state_property'].mean() if df['state_property'].notnull().any() else 0
        mean_b_m = df['B/M'].mean() if df['B/M'].notnull().any() else None
        mean_eps = df['eps'].mean() if df['eps'].notnull().any() else None
        mean_e_p = df['e/p'].mean() if df['e/p'].notnull().any() else None

        companies_data[ticker] = {
            
            
            
            
            
            'mean_net_profit': mean_net_profit,
            'mean_state_property': mean_state_property,
            'mean_b/m': mean_b_m,
            'mean_eps': mean_eps,
            'mean_e/p': mean_e_p,
        }


df = pd.DataFrame(companies_data).T

df = df.to_string(max_colwidth=None)

print("Для нефтегаза:")
print(df)


df = pd.DataFrame(companies_data).T


numeric_df = df.select_dtypes(include='number')


average_values = numeric_df.mean().to_frame().T
average_values['mean_net_profit'] /= 1_000_000

print("Для нефтегаза среднее:")

print(average_values)


print("\n")


companies_data = {}

lst = ['PLZL', 'GMKN', 'NLMK', 'RUAL', 'ALRS', 'MAGN', 'MTLR', 'SELG', 'TRML', 'UGLD']

for ticker in lst:
    if ticker in sheets_dict:
        df = sheets_dict[ticker]

        
        net_profit = df[df['year_month'].str[-2:] == '12']['net_profit'].values[0]

        
        state_property = df[df['year_month'].str[-2:] == '12']['state_property'].values[0]

        
        b_m = df[df['year_month'].str[-2:] == '12']['B/M'].values[0]
        

        
        eps = df[df['year_month'].str[-2:] == '12']['eps'].values[0]

        
        e_p = df[df['year_month'].str[-2:] == '12']['e/p'].values[0]

        
        mean_net_profit = df['net_profit'].mean() if df['net_profit'].notnull().any() else None
        mean_state_property = df['state_property'].mean() if df['state_property'].notnull().any() else 0
        mean_b_m = df['B/M'].mean() if df['B/M'].notnull().any() else None
        mean_eps = df['eps'].mean() if df['eps'].notnull().any() else None
        mean_e_p = df['e/p'].mean() if df['e/p'].notnull().any() else None

        companies_data[ticker] = {
            
            
            
            
            
            'mean_net_profit': mean_net_profit,
            'mean_state_property': mean_state_property,
            'mean_b/m': mean_b_m,
            'mean_eps': mean_eps,
            'mean_e/p': mean_e_p,
        }


df = pd.DataFrame(companies_data).T

df = df.to_string(max_colwidth=None)

print("Для металлов:")
print(df)


df = pd.DataFrame(companies_data).T


numeric_df = df.select_dtypes(include='number')


average_values = numeric_df.mean().to_frame().T
average_values['mean_net_profit'] /= 1_000_000
print("Для металлов среднее:")

print(average_values)
