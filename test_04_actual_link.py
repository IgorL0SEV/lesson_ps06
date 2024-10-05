import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

url = ('https://tomsk.hh.ru/vacancies/programmist')

driver.get(url)
time.sleep(3)

vacancies = driver.find_elements(By.CLASS_NAME, 'vacancy-serp__vacancy')

parsed_data = []

for vacancy in vacancies:
    try:
        title = vacancy.find_element(By.CSS_SELECTOR, 'span.serp-item__title-text').text
        company = vacancy.find_element(By.CSS_SELECTOR, 'span.vacancy-serp__vacancy-employer-text').text
        salary = vacancy.find_element(By.CSS_SELECTOR, 'span.src/components/VacancySearchItem/Compensation/index.tsx:37').text
        link = vacancy.find_element(By.CSS_SELECTOR, 'a.magritte-link___b4rEM_4-3-2').get_attribute('href')
    except:
        print("произошла ошибка при парсинге")
        continue
    parsed_data.append([title, company, salary, link])

driver.quit()

with open('hh_2.csv', 'w', newline = '', encoding = 'utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["название вакансии","компания","зарплата","ссылка"])
    writer.writerows(parsed_data)

