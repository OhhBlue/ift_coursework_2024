"""
TODO -
    - Methods for searching for URLs containing ESG reports of a specific company
        - maybe: google api, openai api, selenium + google search
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from src.data_models.company import Company


class Search:

    def __init__(self, company: Company):
        self.company = company

    def google(self):
        search_query = "+".join(  # noqa: F841
            f"{self.company.security} latest ESG report filetype:pdf".split()
        )
        # TODO - implement google search using selenium
        output = []
        return output


if __name__ == "__main__":
    company = Company(
        symbol="AAPL",
        security="Apple Inc.",
        gics_sector="Technology",
        gics_industry="Technology",
        country="USA",
        region="North America",
    )

    google_results = Search(company).google()

    print(google_results)






"""
Here's the code that uses a Google search and uses Apple as an example
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_csr_links():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)  

    try:
        url = "https://www.google.com/search?q=Apple+Inc.+latest+CSR+report+filetype%3Apdf"
        driver.get(url)

      
        try:
            cookie_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="I agree" or text()="agree"]'))
            )
            cookie_button.click()
        except:
     
            pass

    
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.g")))
        except:
            print("No div.g")
            print(driver.page_source)
            return []

    
        result_elements = driver.find_elements(By.CSS_SELECTOR, "div.g a")
        links = []
        for elem in result_elements:
            href = elem.get_attribute("href")
            if href and href.startswith("http"):
                links.append(href)

        return links

    finally:
        time.sleep(5) 
        driver.quit()

if __name__ == "__main__":
    result_links = scrape_csr_links()
    print("URL：")
    for link in result_links:
        print(link)




"""
This is code that uses a web crawler and uses Apple as an example
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_eleventh_and_get_needed_links(url):
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        print("Opened page:", url)
        all_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        total_links = len(all_links)
        print(f"Found {total_links} <a> tags on the search results page.")
        if total_links < 11:
            print("Not enough links (less than 11) on the page to click the 11th link.")
            return
        eleventh_link = all_links[10]
        print(f"Clicking the 11th link: text='{eleventh_link.text.strip()}', URL={eleventh_link.get_attribute('href')}")
        eleventh_link.click()
        print("Clicked the 11th link, waiting for the company details page to load...")
        company_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        total_company_links = len(company_links)
        print(f"Found {total_company_links} <a> tags on the company details page.")
        needed_links = []
        if total_company_links > 15:
            needed_links.append(company_links[15])
        else:
            print("Not enough links (less than 16) on the company details page.")
        start_idx = 19
        end_idx = total_company_links - 12
        if end_idx >= start_idx:
            for idx in range(start_idx, end_idx + 1):
                ordinal = idx + 1
                if ordinal % 2 == 0:
                    needed_links.append(company_links[idx])
        else:
            print("Not enough links on the company details page to satisfy the range from the 20th link to the 12th from last link.")
        if needed_links:
            print("The required filtered links are:")
            for i, link in enumerate(needed_links):
                text = link.text.strip()
                href = link.get_attribute("href")
                print(f"  Link {i+1}: text='{text}', URL={href}")
        else:
            print("No links satisfy the conditions.")
        return needed_links
    except Exception as e:
        print("Exception occurred:", e)
    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    test_url = "https://www.responsibilityreports.com/Companies?search=apple"
    click_eleventh_and_get_needed_links(test_url)




