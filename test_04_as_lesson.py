import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

url = ('https://tomsk.hh.ru/vacancies/programmist')

driver.get(url)
time.sleep(3)

vacancies = driver.find_elements(By.CLASS_NAME, 'vacancy-card--H8LvOiOGPll0jZvYpxIF')

parsed_data = []

for vacancy in vacancies:
    try:
        title = vacancy.find_element(By.CSS_SELECTOR, 'span.vacancy-name--SYbxrgpHgHedVTkgI_cA').text
        company = vacancy.find_element(By.CSS_SELECTOR, 'span.company-info-text--O32pGCRW0YDmp3BHuNOP').text
        salary = vacancy.find_element(By.CSS_SELECTOR, 'span.compensation-text--cCPBXayRjn5GuLFWhGTJ').text
        link = vacancy.find_element(By.CSS_SELECTOR, 'a.bloko-link').get_attribute('href')
    except:
        print("произошла ошибка при парсинге")
        continue
    parsed_data.append([title, company, salary, link])

driver.quit()

with open('hh.csv', 'w', newline = '', encoding = 'utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["название вакансии","компания","зарплата","ссылка"])
    writer.writerows(parsed_data)
