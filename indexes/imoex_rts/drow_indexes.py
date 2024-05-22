import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def read_data(file_path):
   
    data = pd.read_csv(file_path, delimiter=',', parse_dates=['Дата'], dayfirst=True)

   
    data['Откр.'] = data['Откр.'].str.replace('.', '').str.replace(',', '.').astype(float)

    return data[['Дата', 'Откр.']]


def plot_data(data1, label1, data2, label2):
    plt.figure(figsize=(10, 5))

    plt.plot(data1['Дата'], data1['Откр.'], label=label1, marker='o')
    plt.plot(data2['Дата'], data2['Откр.'], label=label2, marker='o')

   
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[1, 6]))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(''))
    plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter('%b %Y'))

   
    plt.gca().xaxis.set_tick_params(which='major', size=0)
    plt.gca().xaxis.set_tick_params(which='minor', rotation=45)

    plt.title('Динамика цен открытия для ММВБ и РТС')
    plt.xlabel('Дата')
    plt.ylabel('Цена открытия')
    plt.legend()

    plt.gcf().autofmt_xdate() 
    plt.show()



data_mmvb = read_data('Прошлые данные - ММВБ – Индекс Мосбиржи-3.csv')
data_rts = read_data('Прошлые данные - Индекс РТС-2.csv')


plot_data(data_mmvb, 'ММВБ', data_rts, 'РТС')