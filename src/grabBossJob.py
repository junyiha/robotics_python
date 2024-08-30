from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import json
import pandas as pd

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