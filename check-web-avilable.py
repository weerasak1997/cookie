import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  # run without browser UI
chrome_options.add_argument("--lang=en-GB")
chrome_options.add_experimental_option("prefs", {
    "intl.accept_languages": "en-GB"
})
chrome_options.add_argument("--window-size=1920,1080")

service = Service("./chromedriver-mac-x64/chromedriver")  # your driver path
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(20)
driver.set_script_timeout(20)

max_count = 1000000
begin = 21071
row_count = 0

accessible_websites = []

try:
    with open('random_stratified_websites.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_count = int(row['no'])
            if row_count < begin:
                continue
            if row_count > max_count:
                print(f"Reached {max_count} websites limit, stopping.")
                break

            website_no = row['no']
            website_name = row['domain']

            print('------------------')
            print('no', website_no, website_name)

            try:
                driver.get("https://" + website_name)
                # ✅ รอ DOM โหลด
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "html"))
                )
                print(f"✅ Accessible: {website_name}")
                # ✅ เก็บ no, domain ตาม dataset เดิม
                accessible_websites.append({
                    "no": website_no,
                    "domain": website_name
                })

            except TimeoutException:
                print(f"⏳ Timeout loading {website_name}")
            except WebDriverException:
                print(f"❌ Failed to open {website_name}")
            except Exception as e:
                print(f"⚠️ Other Exception on {website_name}: {e}")
finally:
    driver.quit()
    # ✅ บันทึกผลลัพธ์ลงไฟล์ CSV
    with open("accessible_websites.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["no", "domain"])
        writer.writeheader()
        writer.writerows(accessible_websites)

    print(f"Saved {len(accessible_websites)} accessible websites to accessible_websites.csv")
