# pip install selenium beautifulsoup4 lxml webdriver-manager

import time
import csv
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def guess_selectors_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return None

    soup = BeautifulSoup(response.text, "lxml")
    cards = soup.find_all("div", class_=True)

    print("\nАвтоматически найденные карточки товаров:")
    for card in cards[:5]:
        print("=" * 30)
        print(card.text.strip()[:200])  # печатаем текст первых 5 карточек

    return input("\nВведите CSS-селектор карточки товара (например, div.product-card): ").strip(), \
           input("Введите CSS-селектор названия внутри карточки (например, .title): ").strip(), \
           input("Введите CSS-селектор цены внутри карточки (например, .price): ").strip(), \
           input("Введите CSS-селектор ссылки внутри карточки (например, a): ").strip()


def parse_site(url, card_selector, name_selector, price_selector, link_selector):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Без открытия окна браузера

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)

    cards = driver.find_elements(By.CSS_SELECTOR, card_selector)
    print(f"Найдено карточек: {len(cards)}")

    with open("products_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Название", "Цена", "Ссылка"])

        for card in cards:
            try:
                name = card.find_element(By.CSS_SELECTOR, name_selector).text
            except:
                name = "Нет названия"
            try:
                price = card.find_element(By.CSS_SELECTOR, price_selector).text
            except:
                price = "Нет цены"
            try:
                link = card.find_element(By.CSS_SELECTOR, link_selector).get_attribute("href")
            except:
                link = "Нет ссылки"

            print(f"{name} | {price} | {link}")
            writer.writerow([name, price, link])

    driver.quit()
    print("\n✅ Данные сохранены в products_data.csv")


if __name__ == "__main__":
    print("🔍 Универсальный парсер товаров")
    url = input("Введите URL сайта для парсинга: ").strip()

    auto = input("Определить селекторы автоматически? (y/n): ").lower()
    if auto == "y":
        card, name, price, link = guess_selectors_from_url(url)
    else:
        card = input("Введите CSS-селектор карточки товара: ").strip()
        name = input("Введите CSS-селектор названия товара: ").strip()
        price = input("Введите CSS-селектор цены товара: ").strip()
        link = input("Введите CSS-селектор ссылки на товар: ").strip()

    parse_site(url, card, name, price, link)

