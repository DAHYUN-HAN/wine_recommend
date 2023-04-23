from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
import chromedriver_autoinstaller
import os
import csv
import shutil
from urllib import parse
import time
from selenium.webdriver.common.keys import Keys

def check_score(k):
    score = 0
    for i in range(5) :
        class_name = driver.find_element(By.XPATH, '/html/body/section/div[3]/div[2]/div[2]/div[2]/ul/li[{}]/div/a[{}]'.format(k, i+1)).get_attribute('class')
        if(class_name == "on") :
            score += 1
    return score

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument("headless")
    
# Check if chrome driver is installed or not
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

driver_path = f'./{chrome_ver}/chromedriver.exe'
if os.path.exists(driver_path):
    print(f"chrom driver is insatlled: {driver_path}")
else:
    print(f"install the chrome driver(ver: {chrome_ver})")
    chromedriver_autoinstaller.install(True)

# Get driver and open url
driver = webdriver.Chrome(driver_path, options=options)

#웹페이지가 로딩될때까지 기다리고 5초가 넘어가면 웹페이지가 로딩이 안됐더라도 다음 명령어를 실행.
#로딩이 완료되면 그 즉시 다음 명령어로 이동한다.
driver.implicitly_wait(time_to_wait=5)

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36')]
urllib.request.install_opener(opener)

csv_path = "wine_list(5000).csv"

file = open(csv_path, 'r', encoding = 'utf-8-sig')
rdr = csv.reader(file)

# with open('wine_info_detail.csv', 'a', newline='', encoding='utf-8-sig') as f:
#     writer = csv.writer(f)
#     writer.writerow(["이름(한글)", "이름(영어)", "당도", "산도", "바디", "타닌", "아로마", "음식매칭", "상세정보"])

for line in rdr:
    URL = 'https://www.wine21.com/13_search/wine_view.html?Idx={}&lq=LIST'.format(line[1])
    driver.get(url=URL)

    wine_name_kor = driver.find_element(By.XPATH, '/html/body/section/div[3]/div[2]/div[2]/dl/dt').get_attribute('innerText')
    wine_name_eng = driver.find_element(By.XPATH, '/html/body/section/div[3]/div[2]/div[2]/dl/dd').get_attribute('innerText')

    sweet_score = check_score(1)
    acidity_score = check_score(2)
    body_score = check_score(3)
    tannin_score = check_score(4)

    aroma_list = []
    food_list = []
    try : 
        aroma_part = driver.find_element(By.XPATH, '/html/body/section/div[3]/div[2]/div[2]/div[3]/div[1]/div[2]/ul')
        aromas = aroma_part.find_elements(By.CSS_SELECTOR, '.swiper-slide')       

        for aroma in aromas:
            aroma_string = (aroma.find_element(By.TAG_NAME, 'p').get_attribute('innerText'))
            semi_aroma_list = aroma_string.split(",")
            for semi_aroma in semi_aroma_list :
                aroma_list.append(semi_aroma.replace("\xa0", ''))
    
    
        food_part = driver.find_element(By.XPATH, '/html/body/section/div[3]/div[2]/div[2]/div[3]/div[2]/div[2]/ul')
        foods = food_part.find_elements(By.CSS_SELECTOR, '.swiper-slide')

        food_list = []
        for food in foods:
            food_string = (food.find_element(By.TAG_NAME, 'p').get_attribute('innerText'))
            semi_food_list = food_string.split(",")
            for semi_food in semi_food_list :
                food_list.append(semi_food.replace("\xa0", ''))
    except :
        continue

    detail_part = driver.find_element(By.XPATH, '//*[@id="detail"]/div/div')

    detail_dict = {}
    detail_list = detail_part.find_elements(By.TAG_NAME, 'dl')
    for detail in detail_list :
        detail_dict[detail.find_element(By.TAG_NAME, 'dt').get_attribute('innerText')] = detail.find_element(By.TAG_NAME, 'dd').get_attribute('innerText').replace("\xa0", "")

    with open('wine_info_detail.csv', 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([wine_name_kor, wine_name_eng, sweet_score, acidity_score, body_score, tannin_score, aroma_list, food_list, detail_dict])