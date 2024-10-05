import requests
from bs4 import BeautifulSoup
import csv

# URL для парсинга
url = "https://www.divan.ru/category/divany"

# Отправляем запрос к сайту
response = requests.get(url)

# Проверяем успешность запроса
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Открываем CSV файл для записи
    with open('divan_data_var_1.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Пишем заголовки
        writer.writerow(['Название', 'Цена', 'Ссылка'])

        # Ищем карточки продуктов
        product_cards = soup.find_all('div', {'data-testid': 'product-card'})

        for card in product_cards:
            # Парсим название
            name_tag = card.find('span', itemprop='name')
            name = name_tag.text.strip() if name_tag else 'Название не найдено'

            # Парсим цену
            price_tag = card.find('span', {'data-testid': 'price'})
            price = price_tag.text.strip() if price_tag else 'Цена не найдена'

            # Парсим ссылку
            link_tag = card.find('a', class_='ui-GPFV8')
            link = "https://www.divan.ru" + link_tag['href'] if link_tag else 'Ссылка не найдена'

            # Пишем данные в CSV файл
            writer.writerow([name, price, link])
            print([name, price, link])

    print("Данные успешно сохранены в файл 'divan_data_var_1.csv'")
else:
    print(f"Ошибка при запросе страницы: {response.status_code}")
