from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import json
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree

def GrabJobV1():
    driver = webdriver.Edge()

    driver.get("https://www.zhipin.com/web/geek/job?query=C%2B%2B&city=100010000")

    driver.delete_all_cookies()

    with open('cookies.txt', 'r') as f:
        cookies_list = json.load(f)
        
        for cookie in cookies_list:
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)

    time.sleep(10)

    tags_li = driver.find_elements(by=By.XPATH, value="//li[@class='job-card-wrapper']")

    time.sleep(15)

    job_data = []

    for li in tags_li:
        title_tag = li.find_elements(By.CSS_SELECTOR, ".job-name")  # 标题
        area_tag = li.find_elements(By.CSS_SELECTOR, ".job-area-wrapper")  # 地区
        salary_tag = li.find_elements(By.CSS_SELECTOR, ".salary")  # 工资
        name_tag = li.find_elements(By.CSS_SELECTOR, ".company-name")  # 公司名称
        desc_tag = li.find_elements(By.CSS_SELECTOR, ".info-desc")  # 详情

        job_title = [i.text for i in title_tag]
        job_area = [x.text for x in area_tag]
        job_salary = [x.text for x in salary_tag]
        job_name = [x.text for x in name_tag]
        job_desc = [x.text for x in desc_tag]

        print(job_title,job_area,job_salary,job_name,job_desc)
        dict = {
            '岗位': job_title,
            '地址': job_area,
            '工资': job_salary,
            '公司名称': job_name,
            '详情': job_desc,
        }
        job_data.append(dict)
    df = pd.DataFrame(job_data)
    df.to_excel('boss直聘爬虫.xlsx', index=False)

    #  休眠10秒
    time.sleep(10)

    driver.close()
    driver.quit()
    

def ParseHTMLText(text):
    root = etree.HTML(text)
    br_tags = root.xpath('//br')
    data = ""
    for br in br_tags:
        previous_text = br.tail.strip() if br.tail else "[No text after <br>]"
        data += previous_text
        data += "\n"
        
    return data
    
def GrabJobInformation(link_list):
    driver = webdriver.Edge()
    text_list = []
    for link in link_list:
        driver.get(link)
        driver.delete_all_cookies()

        with open('cookies.txt', 'r') as f:
            cookies_list = json.load(f)
            
            for cookie in cookies_list:
                if isinstance(cookie.get('expiry'), float):
                    cookie['expiry'] = int(cookie['expiry'])
                driver.add_cookie(cookie)
        time.sleep(5)
        text = driver.page_source
        text_list.append(text)

    data_list = []
    for text in text_list:
        soup = BeautifulSoup(text, 'html.parser')
        job_sec_text = soup.find_all(class_ = 'job-sec-text')
        data = ParseHTMLText(str(job_sec_text))
        data_list.append(data)
    
    with open('jobInformation.txt', 'wb') as f:
        for data in data_list:
            data = data.encode()
            f.write(data)

def GrabJobV2():
    driver = webdriver.Edge()

    driver.get("https://www.zhipin.com/web/geek/job?query=C%2B%2B&city=100010000")

    driver.delete_all_cookies()

    with open('cookies.txt', 'r') as f:
        cookies_list = json.load(f)
        
        for cookie in cookies_list:
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)

    time.sleep(5)
    text = driver.page_source
    soup = BeautifulSoup(text, 'html.parser')

    job_card_left_elements = soup.find_all(class_ = 'job-card-left')
    full_link_list = []
    for element in job_card_left_elements:
        href = element['href']
        full_link = 'https://www.zhipin.com' + href
        full_link_list.append(full_link)
    
    GrabJobInformation(full_link_list)


GrabJobV2()
# ParseHTMLText()