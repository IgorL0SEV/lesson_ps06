#📌 1. Импорт библиотек:
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Эти модули используются для:
# selenium — автоматизация браузера.
# csv — сохранение результатов.
# WebDriverWait, EC — ожидание элементов на странице.
# ChromeDriverManager — автоматическая установка драйвера Chrome.


#📌 2. Функция init_driver()
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Запуск в фоне (без окна браузера)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 🔸 Что делает:
# Создаёт и настраивает браузер Chrome.
# --headless — чтобы окно не открывалось.
# Возвращает готовый driver, который используется для открытия сайта.


# 3. Функция wait_for_products(driver)
def wait_for_products(driver):
    return WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='product-card']"))
    )

# 🔸 Что делает:
# Ожидает (до 15 секунд), пока на странице появятся карточки товаров.
# Используется вместо time.sleep() — более надёжно и быстро.


#📌 4. Функция parse_page(driver)
def parse_page(driver):
    products = wait_for_products(driver)
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
            link = product.find_element(By.XPATH, ".//a[contains(@class,'ui-GPFV8')]").get_attribute('href')
        except:
            link = "Нет ссылки"

        result.append([name, price, link])

    return result

# 🔸 Что делает:
# Находит все карточки.
# Из каждой карточки:
# Забирает название, цену, ссылку.
# Добавляет в список result как строку: [название, цена, ссылка].


#📌 5. Функция go_to_next_page(driver)
def go_to_next_page(driver):
    try:
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@aria-label,'Следующая страница')]"))
        )
        driver.execute_script("arguments[0].click();", next_btn)
        return True
    except:
        return False

# 🔸 Что делает:
# Ищет кнопку "Следующая страница" и кликает по ней.
# Если кнопка не найдена (страница последняя) — возвращает False, и парсинг останавливается.


#📌 6. Главная функция main()
def main():
    driver = init_driver()
    driver.get("https://www.divan.ru/category/divany")
    all_data = []

    page = 1
    while True:
        print(f"Парсим страницу {page}...")
        all_data += parse_page(driver)

        if not go_to_next_page(driver):
            break
        page += 1

    driver.quit()

    with open("divans_data.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Цена', 'Ссылка'])
        writer.writerows(all_data)

    print(f"✅ Всего товаров сохранено: {len(all_data)}")
    print("💾 Данные успешно записаны в divans_data.csv")

# 🔸 Что делает:
# Открывает первую страницу.
# Запускает цикл, пока есть кнопка "Следующая страница":
# Парсит текущую страницу.
# Добавляет данные в список all_data.
# После завершения:
# Закрывает браузер.
# Сохраняет данные в CSV.

