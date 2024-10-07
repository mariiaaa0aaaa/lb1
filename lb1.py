import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from datetime import datetime


# Функція для отримання курсу валют за період
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
            print(f"Could not parse XML response. Response text: {response.text}")
            return None, None
    else:
        print(f"Error: Received status code {response.status_code}.")
        return None, None


# Функція для виведення курсу валют на консоль
def print_currency_rates():
    dates, rates = get_currency_rates_for_week()

    if dates and rates:
        print("Currency rates for USD from 30.09.2024 to 06.10.2024:")
        for date, rate in zip(dates, rates):
            print(f"Date: {date.strftime('%d.%m.%Y')}, Rate: {rate}")


# Побудувати графік зміни курсу валюти
def plot_currency_rate():
    dates, rates = get_currency_rates_for_week()

    if dates and rates:
        plt.figure(figsize=(10, 5))
        plt.plot(dates, rates, marker='o', label='USD Rate')

        # Додаємо цифрові показники курсів на графік
        for i, txt in enumerate(rates):
            plt.annotate(f'{txt:.4f}', (dates[i], rates[i]), textcoords="offset points", xytext=(0, 5), ha='center')

        plt.title('USD Exchange Rate (30.09.2024 - 06.10.2024)')
        plt.xlabel('Date')
        plt.ylabel('Rate (UAH)')
        plt.grid(True)
        plt.ylim(41.150, 41.4)  # Шкала для більш детального відображення
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()


# Виклик функції для виведення на консоль і побудови графіка
print_currency_rates()  # Виведення курсу на консоль
plot_currency_rate()  # Побудова графіка