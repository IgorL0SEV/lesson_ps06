import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Настройка веб-драйвера Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Запуск браузера в фоновом режиме
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Открытие страницы сайта
driver.get('https://www.divan.ru/category/divany')

time.sleep(10)  # Ожидание загрузки страницы

# Поиск карточек товаров
products = driver.find_elements(By.XPATH, "//div[@data-testid='product-card']")

# Открытие CSV файла для записи
with open('divans_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название', 'Цена', 'Ссылка'])

    # Парсинг данных с каждой карточки товара
    for product in products:
        # Название дивана
        try:
            name = product.find_element(By.XPATH, ".//a[@class='ui-GPFV8 qUioe ProductName ActiveProduct']/span").text
        except:
            name = "Нет названия"

        # Цена дивана
        try:
            price = product.find_element(By.XPATH, ".//span[@data-testid='price']").text
        except:
            price = "Нет цены"

        # Ссылка на диван
        try:
            link = product.find_element(By.XPATH, ".//a[@class='ui-GPFV8']").get_attribute('href')
        except:
            link = "Нет ссылки"

        # Запись данных в CSV файл
        writer.writerow([name, price, link])
        print([name, price, link])
# Закрытие драйвера
driver.quit()

print("Данные успешно сохранены в divans_data.csv")
