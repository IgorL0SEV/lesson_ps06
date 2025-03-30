# ✅ Что делает код:
# Открывает сайт по заданному URL.
# Автоматически находит карточки товаров.
# Ищет внутри карточки текст, похожий на цену (по наличию символа ₽).
# Находит первую ссылку (<a>).
# Сохраняет результат в auto_parsed_divans.csv.

import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Указываем URL сайта
url = input("Введите URL сайта для парсинга: ")

# Настройка Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # фоновый режим
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Открываем страницу
driver.get(url)
time.sleep(10)  # Подождать загрузку

# Находим все потенциальные карточки товаров
cards = driver.find_elements(By.XPATH, "//*[contains(@data-testid, 'product-card') or contains(@class, 'product') or contains(@class, 'card')]")

results = []

for card in cards:
    try:
        name = card.find_element(By.XPATH, ".//span").text
    except:
        name = "Название не найдено"

    try:
        price = next((el.text for el in card.find_elements(By.XPATH, ".//span") if "₽" in el.text), "Цена не найдена")
    except:
        price = "Цена не найдена"

    try:
        link = card.find_element(By.XPATH, ".//a").get_attribute("href")
    except:
        link = "Ссылка не найдена"

    results.append([name, price, link])
    print(name, price, link)

# Сохраняем результат
with open("auto_parsed_output.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Название", "Цена", "Ссылка"])
    writer.writerows(results)

driver.quit()
print("✅ Данные сохранены в auto_parsed_output.csv")

