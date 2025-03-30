import time
import csv
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Важно: если headless=False, ты увидишь, как браузер открывается и щёлкает по страницам.
# Если headless=True, всё произойдёт в фоне.


# Настройка логирования
def setup_logger():
    logging.basicConfig(
        filename='parser.log',
        filemode='a',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


# Инициализация драйвера
def init_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Ожидание загрузки карточек товара
def wait_for_products(driver, timeout=15):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-testid='product-card']"))
    )


# Парсинг одной страницы
def parse_page(driver):
    products = driver.find_elements(By.XPATH, "//div[@data-testid='product-card']")
    result = []

    for product in products:
        try:
            name = product.find_element(By.XPATH, ".//a[contains(@class,'ProductName')]/span").text
        except:
            name = "Нет названия"

        try:
            price = product.find_element(By.XPATH, ".//span[@data-testid='price']").text
        except:
            price = "Нет цены"

        try:
            link = product.find_element(By.XPATH, ".//a[contains(@class,'ProductName')]").get_attribute("href")
        except:
            link = "Нет ссылки"

        result.append((name, price, link))
    return result


# Переход на следующую страницу
def go_to_next_page(driver):
    try:
        next_button = driver.find_element(By.XPATH, "//a[contains(@class, 'PaginationButton') and contains(text(),'Следующая')]")
        next_button.click()
        time.sleep(3)
        return True
    except NoSuchElementException:
        return False


# Сохранение в CSV
def save_to_csv(data):
    filename = f"divans_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Цена', 'Ссылка'])
        writer.writerows(data)
    print(f"✅ Данные сохранены в файл: {filename}")


# Основной процесс
def main():
    setup_logger()
    print("💬 Парсинг диванов с divan.ru")

    mode = input("🔹 Хотите видеть работу браузера? (y/n): ").lower().strip()
    headless = mode != 'y'

    driver = init_driver(headless=headless)
    driver.get("https://www.divan.ru/category/divany")

    try:
        wait_for_products(driver)
        all_data = []

        while True:
            logging.info("📄 Парсинг страницы")
            data = parse_page(driver)
            all_data.extend(data)

            if not go_to_next_page(driver):
                break

        save_to_csv(all_data)
        logging.info("✅ Парсинг завершен успешно.")
        print("✅ Готово! Проверьте CSV файл.")

    except TimeoutException:
        logging.error("❌ Превышено время ожидания загрузки карточек товаров.")
        print("Ошибка: Страница не загрузилась вовремя.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

# 📌 Что делает этот код:
# Загружает сайт divan.ru/category/divany.
# Парсит все страницы каталога с диванами.
# Собирает:
# Название
# Цену
# Ссылку на товар
# Сохраняет в CSV-файл с текущей датой.
# Пишет логи в parser.log.

