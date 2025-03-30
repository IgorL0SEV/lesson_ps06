import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Инициализация браузера
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Фоновый режим
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Ожидание загрузки карточек товаров
def wait_for_products(driver):
    return WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='product-card']"))
    )

# Парсинг одной страницы
def parse_page(driver):
    products = wait_for_products(driver)
    result = []

    for product in products:
        # Название
        try:
            name = product.find_element(By.XPATH, ".//a[contains(@class,'ProductName')]/span").text
        except:
            name = "Нет названия"

        # Цена
        try:
            price = product.find_element(By.XPATH, ".//span[@data-testid='price']").text
        except:
            price = "Нет цены"

        # Ссылка
        try:
            link = product.find_element(By.XPATH, ".//a[contains(@class,'ui-GPFV8')]").get_attribute('href')
        except:
            link = "Нет ссылки"

        result.append([name, price, link])

    return result

# Переход на следующую страницу
def go_to_next_page(driver):
    try:
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@aria-label,'Следующая страница')]"))
        )
        driver.execute_script("arguments[0].click();", next_btn)
        return True
    except:
        return False

# Основной запуск
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

    # Запись в CSV
    with open("divans_data.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Цена', 'Ссылка'])
        writer.writerows(all_data)

    print(f"✅ Всего товаров сохранено: {len(all_data)}")
    print("💾 Данные успешно записаны в divans_data.csv")

if __name__ == "__main__":
    main()
