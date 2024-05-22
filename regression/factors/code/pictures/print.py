import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


df = pd.read_excel('data_for_reg_upt_upt.xlsx')
df = pd.read_excel('data_for_reg_upt_upt_1.xlsx')
df = pd.read_excel('upt_blue_for_reg_with_wsoe.xlsx')
df = pd.read_excel('upt_blue_for_reg_with_dogs (13).xlsx')


df['date'] = pd.to_datetime(df['date']).dt.to_period('M')


df['WSMB_ALL'] *= 100


df['SMA_6'] = df['WSMB_ALL'].rolling(window=6).mean()


plt.figure(figsize=(12, 6))


plt.plot(df['date'].dt.to_timestamp(), df['WSMB_ALL'], label='SMB (%)', marker='o', linestyle='-', color='lightblue')
plt.plot(df['date'].dt.to_timestamp(), df['SMA_6'], label='6-Month SMA', color='red', linestyle='--', linewidth=2)


plt.title('Значение фактора SMB и скользящее среднее за 6 месяцев')
plt.xlabel('Дата')
plt.ylabel('SMB (%)')
plt.legend()


plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 6)))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gcf().autofmt_xdate(rotation=45)


plt.grid(True)
plt.tight_layout()
plt.show()