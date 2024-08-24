from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_website(url):
    """
    Connect to the website and scrape data from the list of members.
    """
    try:
        print(f"Connecting to {url}...")
        service = Service('/usr/local/bin/chromedriver')
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        print("Connection successful!")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        print(f"Page title: {driver.title}")

        select_length = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'MemberListTable_length'))
        )
        select_length.click()
        time.sleep(0.5)
        option_100 = select_length.find_element(By.XPATH, "//option[@value='100']")
        option_100.click()
        print("Set entries to 100")

        time.sleep(5)

        all_data = []
        current_id = 1
        while True:
            try:
                member_table = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, 'MemberListTable'))
                )
                print("Found member table")
            except Exception as e:
                print(f"Could not find member table: {e}")
                with open('page_source.html', 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                print("Saved page source to page_source.html")
                raise

            rows = member_table.find_elements(By.TAG_NAME, 'tr')
            for i in range(1, len(rows)):
                columns = rows[i].find_elements(By.TAG_NAME, 'td')
                if columns:
                    name = columns[0].text.strip()
                    print(f"Name: {name}")

                    more_details = columns[2].find_element(By.TAG_NAME, 'span')
                    more_details.click()
                    time.sleep(2)

                    detail_row = rows[i].find_element(By.XPATH, './following-sibling::tr[1]')
                    detail_columns = detail_row.find_elements(By.CLASS_NAME, 'detail')
                    if detail_columns:
                        additional_info = {'Name': name}
                        for detail in detail_columns:
                            detail_data = detail.find_elements(By.TAG_NAME, 'span')
                            for j in range(0, len(detail_data), 2):
                                label = detail_data[j].text.strip()
                                value = detail_data[j + 1].text.strip() if j + 1 < len(detail_data) else "N/A"
                                additional_info[label] = value

                        additional_info['ID'] = current_id

                        all_data.append(additional_info)
                        print(f"Details extracted: {additional_info}")

                        current_id += 1

                    close_details = detail_row.find_element(By.TAG_NAME, 'span')
                    close_details.click()
                    time.sleep(0.25)

            with open('member_list_data.json', 'w') as json_file:
                json.dump(all_data, json_file, indent=4)
            print(f"Data saved to member_list_data.json after processing {len(all_data)} rows")

            try:
                next_page = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'paginate_button') and text()='2']"))
                )
                next_page.click()
                time.sleep(5)
            except Exception as e:
                print("No more pages to process.")
                break

    except Exception as e:
        raise Exception(f"Failed to process {url}: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

url = os.getenv("EXHIBITORS_URL")
connect_to_website(url)