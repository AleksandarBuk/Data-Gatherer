from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import json
import time

def safe_find_element(parent, by, value):
    """
    Safely find an element within a parent element.
    """
    try:
        return parent.find_element(by, value)
    except NoSuchElementException:
        return None

def connect_to_website(url):
    """
    Connect to the website and scrape data from the list of exhibitors.
    """
    try:
        print(f"Connecting to {url}...")
        service = Service('/path/to/chromedriver')
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        print("Connection successful!")

        time.sleep(10)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'pagecontent'))
        )
        print(f"Page title: {driver.title}")

        all_data = []
        current_id = 1

        while True:
            try:
                items = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.item'))
                )
                print(f"Found {len(items)} items on the current page.")

                for index in range(len(items)):
                    try:
                        items = driver.find_elements(By.CSS_SELECTOR, '.item')
                        item = items[index]

                        item_link = safe_find_element(item, By.CSS_SELECTOR, 'a')
                        if not item_link:
                            print(f"Item link not found for item {index + 1}")
                            continue

                        item_name = item_link.text.strip()
                        item_country = safe_find_element(item, By.CSS_SELECTOR, '.col1ergebnis p')
                        item_country_text = item_country.text.strip() if item_country else "N/A"
                        item_hall_stand = safe_find_element(item, By.CSS_SELECTOR, '.col3ergebnis a span')
                        item_hall_stand_text = item_hall_stand.text.strip() if item_hall_stand else "N/A"
                        item_description = safe_find_element(item, By.CSS_SELECTOR, '.inner')
                        item_description_text = item_description.text.split('\n')[-1].strip() if item_description else "N/A"

                        driver.execute_script("arguments[0].click();", item_link)
                        time.sleep(2)

                        additional_details = safe_find_element(driver, By.CSS_SELECTOR, '.additional-details')
                        additional_details_text = additional_details.text.strip() if additional_details else "N/A"

                        company_name = safe_find_element(driver, By.CSS_SELECTOR, '.headline-title span')
                        company_name_text = company_name.text.strip() if company_name else "N/A"
                        location_info = safe_find_element(driver, By.CSS_SELECTOR, '.location-info')
                        company_address_text = location_info.text.strip() if location_info else "N/A"
                        company_phone = safe_find_element(driver, By.CSS_SELECTOR, '.ico_phone')
                        company_phone_text = company_phone.text.strip() if company_phone else "N/A"
                        company_email = safe_find_element(driver, By.CSS_SELECTOR, '.ico_email a')
                        company_email_text = company_email.get_attribute('href').replace('mailto:', '').strip() if company_email else "N/A"
                        company_website = safe_find_element(driver, By.CSS_SELECTOR, '.ico_link a')
                        company_website_text = company_website.get_attribute('href').strip() if company_website else "N/A"

                        hall_stand_info = safe_find_element(driver, By.CSS_SELECTOR, '.asdb54-hallen-bubble .texts')
                        hall_stand_info_text = hall_stand_info.text.strip() if hall_stand_info else "N/A"

                        company_description = safe_find_element(driver, By.CSS_SELECTOR, '.werbetext54')
                        company_description_text = company_description.text.strip() if company_description else "N/A"

                        driver.back()
                        time.sleep(5)

                        additional_info = {
                            'ID': current_id,
                            'Name': item_name,
                            'Country': item_country_text,
                            'Hall_Stand': hall_stand_info_text,
                            'Description': company_description_text,
                            'Additional_Details': additional_details_text,
                            'Company_Name': company_name_text,
                            'Company_Address': company_address_text,
                            'Company_Phone': company_phone_text,
                            'Company_Email': company_email_text,
                            'Company_Website': company_website_text
                        }
                        all_data.append(additional_info)
                        print(f"Details extracted: {additional_info}")

                        current_id += 1

                    except Exception as e:
                        print(f"Error extracting data for item {index + 1}: {e}")

                with open('third_site_output.json', 'w') as json_file:
                    json.dump(all_data, json_file, indent=4)
                print(f"Data saved to third_site_output.json after processing {len(all_data)} entries")

                try:
                    next_page = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[@rel='next']"))
                    )
                    driver.execute_script("arguments[0].click();", next_page)
                    print("Navigated to the next page.")
                    time.sleep(5)
                except TimeoutException:
                    print("No more pages to process or error finding next page.")
                    break

            except Exception as e:
                print(f"Error processing exhibitor list on the current page: {e}")
                break

    except Exception as e:
        print(f"Failed to process {url}: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            print("Driver closed.")

from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("EXHIBITORS_URL")
connect_to_website(url)