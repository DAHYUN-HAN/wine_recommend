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

URL = 'https://www.wine21.com/13_search/wine_list.html'
driver.get(url=URL)

i = 0
wine_list = []
while(True) :
    try :
        i += 1
        
        javascript_url = driver.find_element(By.XPATH, '//*[@id="wine_list"]/li[{}]/div[2]/div[1]/h3/a'.format(i)).get_attribute('href')
        wine_name = driver.find_element(By.XPATH, '//*[@id="wine_list"]/li[{}]/div[2]/div[1]/h3/a'.format(i)).get_attribute('innerText')
        wine_name = wine_name.replace("\n", " ")
        num = javascript_url.split("(")[-1].split(")")[0]

        wine_list.append([wine_name, num])
        with open('wine_list.csv', 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([wine_name, num])

        if(i % 10 == 0) :
            driver.find_element(By.ID, 'wineListMoreBtn').click()
            for down in range(5):
                driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
            if(driver.current_url == "https://www.wine21.com/17_company/company_privacy.html") :
                driver.back()
    except :
        if(len(wine_list) > 28200) :
            break
        continue

with open('wine_list_final.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(wine_list)

# for menu in menus:
#     if(menu.get_attribute('innerText') == "기본정보") :
#         parent_el = menu.find_element(By.XPATH, '..')
#         grand_el = parent_el.find_element(By.XPATH, '..')
#         info_url = grand_el.find_element(By.TAG_NAME, 'a').get_attribute('href')
#     elif(menu.get_attribute('innerText') == "포토") :
#         parent_el = menu.find_element(By.XPATH, '..')
#         grand_el = parent_el.find_element(By.XPATH, '..')
#         photo_url = grand_el.find_element(By.TAG_NAME, 'a').get_attribute('href')

# if(info_url in check_list) :
#     with open('pass_list3.csv', 'a', newline='', encoding='utf-8-sig') as f:
#         writer = csv.writer(f)
#         writer.writerow(line)
#     continue
# else:
#     check_list.append(info_url)
    
# if(photo_url in check_list) :
#     with open('pass_list3.csv', 'a', newline='', encoding='utf-8-sig') as f:
#         writer = csv.writer(f)
#         writer.writerow(line)
#     continue
# else:
#     check_list.append(photo_url)
    
# time.sleep(1)
# driver.get(url=info_url)

# try :
#     movie_name = driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[2]/div[1]/div[1]/h2/span/strong').get_attribute('innerText')
#     image_name = movie_name.replace('\\', '')
#     image_name = image_name.replace('/', '')
#     image_name = image_name.replace(':', '')
#     image_name = image_name.replace('*', '')
#     image_name = image_name.replace('?', '')
#     image_name = image_name.replace('"', '')
#     image_name = image_name.replace('<', '')
#     image_name = image_name.replace('>', '')
#     image_name = image_name.replace('|', '')
# except :
#     print("영화 정보 없음")
#     continue

# detail_info = driver.find_element(By.CSS_SELECTOR, '.detail_info')
# info_groups = detail_info.find_elements(By.CSS_SELECTOR, '.info_group')
# year = ""
# distributor = ""
# for info_group in info_groups :
#     if(info_group.find_element(By.TAG_NAME, 'dt').get_attribute('innerText') == "개봉") :
#         year = info_group.find_element(By.TAG_NAME, 'dd').get_attribute('innerText').split(".")[0]
#     elif(info_group.find_element(By.TAG_NAME, 'dt').get_attribute('innerText') == "배급") :
#         distributor = info_group.find_element(By.TAG_NAME, 'dd').get_attribute('innerText')

# time.sleep(1)

# driver.get(url=photo_url)
# poster_group = driver.find_element(By.CSS_SELECTOR, '._image_base_poster')
# poster_part = poster_group.find_element(By.CSS_SELECTOR, '.movie_photo_list')
# poster_list = poster_part.find_elements(By.CSS_SELECTOR, '.item')

# image_name_list = []
# for i, poster in enumerate(poster_list) :
#     image_info =poster.find_element(By.TAG_NAME, 'a').get_attribute("innerHTML")
#     image_src = image_info.split('data-img-src="')[-1].split('"')[0]
#     image_src.replace("quality=75", "quality=100")
#     download_name = "{}_{}.jpg".format(image_name, i+1)
#     urllib.request.urlretrieve(image_src, "image/" + download_name)
#     image_name_list.append(download_name)

# info_list = [movie_name, year, distributor, image_name_list]
# time.sleep(2)

# with open('movie_info_retry.csv', 'a', newline='', encoding='utf-8-sig') as f:
#     writer = csv.writer(f)
#     writer.writerow(info_list)