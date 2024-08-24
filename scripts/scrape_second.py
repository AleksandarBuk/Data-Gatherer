from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import os

load_dotenv()

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
        service = Service('/usr/local/bin/chromedriver')
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        print("Connection successful!")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'exh-list'))
        )
        print(f"Page title: {driver.title}")

        all_data = []
        current_id = 1
        while True:
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'broaditem'))
                )
                print("Found exhibitor items")

                broad_items = driver.find_elements(By.CLASS_NAME, 'broaditem')
                if broad_items:
                    for item in broad_items:
                        try:
                            name_element = safe_find_element(item, By.CLASS_NAME, 'broadname')
                            stand_element = safe_find_element(item, By.CLASS_NAME, 'broadStandNo')
                            
                            name = name_element.text.strip() if name_element else "N/A"
                            stand_number = stand_element.text.strip() if stand_element else "N/A"
                            print(f"Name: {name}, Stand Number: {stand_number}")

                            item_link = safe_find_element(item, By.CLASS_NAME, 'broaditemlink')
                            if item_link:
                                driver.execute_script("arguments[0].click();", item_link)
                            else:
                                driver.execute_script("arguments[0].click();", item)
                            time.sleep(2)

                            infobox = WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.ID, 'infobox'))
                            )
                            
                            additional_info = {'Name': name, 'Stand Number': stand_number}
                            
                            company_info = safe_find_element(infobox, By.ID, 'companyinfo2')
                            additional_info['Company Info'] = company_info.text if company_info else "N/A"
                            
                            information = safe_find_element(infobox, By.ID, 'companyinfo')
                            additional_info['Information'] = information.text if information else "N/A"
                            
                            product_categories = safe_find_element(infobox, By.ID, 'companyinfo4')
                            additional_info['Product Categories'] = product_categories.text if product_categories else "N/A"
                            
                            brand_names = safe_find_element(infobox, By.ID, 'companyinfo5')
                            additional_info['Brand Names'] = brand_names.text if brand_names else "N/A"

                            additional_info['ID'] = current_id

                            all_data.append(additional_info)
                            print(f"Details extracted: {additional_info}")

                            current_id += 1

                            driver.back()
                            time.sleep(2)

                        except Exception as e:
                            print(f"Error extracting data for an item: {e}")

                    with open('second_member_list_data.json', 'w') as json_file:
                        json.dump(all_data, json_file, indent=4)
                    print(f"Data saved to second_member_list_data.json after processing {len(all_data)} entries")

                try:
                    next_page = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Next')]"))
                    )
                    driver.execute_script("arguments[0].click();", next_page)
                    time.sleep(5)
                except Exception as e:
                    print("No more pages to process or error finding next page: ", e)
                    break

            except Exception as e:
                print(f"Error processing exhibitor list: {e}")
                break

    except Exception as e:
        print(f"Failed to process {url}: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            print("Driver closed.")

url = os.getenv("EXHIBITORS_URL")
connect_to_website(url)
