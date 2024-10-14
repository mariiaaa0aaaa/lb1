import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates  # Додаємо модуль для роботи з датами

print(f"----------- Завдання 1- 3 -----------")
# отримання курсу валют за тиждень
def get_currency_rates_for_week():
    url = 'https://bank.gov.ua/NBU_Exchange/exchange_site?start=20240930&end=20241006&valcode=usd&sort=exchangedate&order=asc'
    response = requests.get(url)

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.content)
            dates = []
            rates = []

            for currency in root.findall('currency'):
                date = currency.find('exchangedate').text
                rate = float(currency.find('rate').text)
                dates.append(datetime.strptime(date, '%d.%m.%Y'))
                rates.append(rate)

            return dates, rates
        except ET.ParseError:
            print(f"Не вдалося розібрати XML-відповідь. Текст відповіді: {response.text}")
            return None, None
    else:
        print(f"Помилка: Отримано код статусу {response.status_code}.")
        return None, None


# Функція для виведення курсу валют на консоль
def print_currency_rates():
    dates, rates = get_currency_rates_for_week()

    if dates and rates:
        print("Курси валют для USD від 30.09.2024 до 06.10.2024:")
        for date, rate in zip(dates, rates):
            print(f"Дата: {date.strftime('%d.%m.%Y')}, Курс: {rate}")


# графік зміни курсу
def plot_currency_rate():
    dates, rates = get_currency_rates_for_week()

    if dates and rates:
        plt.figure(figsize=(10, 5))
        plt.plot(dates, rates, marker='o', label='Курс долара США')

        # цифрові показники курсів на графік
        for i, txt in enumerate(rates):
            plt.annotate(f'{txt:.4f}', (dates[i], rates[i]), textcoords="offset points", xytext=(0, 5), ha='center')

        plt.title('Курс долара США (30.09.2024 - 06.10.2024)')
        plt.xlabel('Дата')
        plt.ylabel('Курс (UAH)')
        plt.grid(True)
        plt.ylim(41.150, 41.4)  # зміна вигляду шкали по ігріку

        # вигляд дат на осі ікс
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

print_currency_rates()  # виведення курсу на консоль
plot_currency_rate()  # побудова графіка