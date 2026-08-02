#!/usr/bin/env python 

# ref :  https://www.scrapingbee.com/blog/selenium-python/


import os
import sys
import time

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    options = ChromeOptions()
    options.add_argument("--headless=new")  # Modern headless flag
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # Helpful for avoiding bot detection in some environments
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def run_declaration():
    # Load Config from Environment Variables
    # Use .get() to provide a fallback or None
    config = {
        "website_url": os.getenv("WEBSITE_URL", "https://etemptation.ville-noumea.nc"),
        "username":    os.getenv("USERNAME"),
        "password":    os.getenv("PASSWORD"),
        "browser":     os.getenv("BROWSER", "chrome") # Default to chrome
    }

    # Validation: Ensure required variables are present
    required_keys = ["username", "password"]
    for key in required_keys:
        if not config[key]:
            print(f"ERROR: Environment variable {key.upper()} is not set.")
            exit(1)

    browser = get_driver()
    wait = WebDriverWait(browser, 10)

    try:
        # Navigation
        browser.get(config['website_url'])

        # Login
        wait.until(EC.presence_of_element_located((By.ID, "usernameLogin"))).send_keys(config["username"])
        wait.until(EC.presence_of_element_located((By.ID, "passwordLogin"))).send_keys(config["password"])
        wait.until(EC.presence_of_element_located((By.ID, "connectBtn"))).click()

        time.sleep(1)
        disconnect = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="header"]/div[2]/div[1]/button/span')))
        print("Successfully logged in.")

        # Navigate to Lunch Tickets
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="page-dashboard"]/div/div[3]/div/div[3]/div[1]/a'))).click()
        wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Titre '))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rf-itempanel-counters"]/div/div[1]/div/div/div/div/div/div/div/span'))).click()

        # Fill Form
        browser.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/main/div/div[1]/div[1]/div[2]/div/div[2]/form/div[3]/div[1]/div[2]/div[1]/div/input').send_keys(datetime.today().strftime("%d/%m/%Y"))
        browser.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/main/div/div[1]/div[1]/div[2]/div/div[2]/form/div[6]/div[2]/button').click()

        time.sleep(2)
        alert_message = None
        validation_message = None
        error = False

        try:
            elements = browser.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div[1]/span')
            if elements and elements[0].is_displayed():
                validation_message = elements[0].text
        except Exception as e:
            print(f"Error validation: {e}.")
            error = True

        try:
            elements = browser.find_elements(By.XPATH, '/html/body/div[1]/div[3]/div/main/div/div[1]/div[1]/div[2]/div/div[2]/form/div[2]/div/div[2]/div[2]')
            if elements and elements[0].is_displayed():
                alert_message = elements[0].text
        except Exception as e:
            print(f"Error alert: {e}.")
            error = True

        if validation_message:
            print("Success: Declaration submitted.")
        elif alert_message:
            print("Error: Solde insuffisant.")
        else:
            print("Erreur inconnue")

        disconnect.click()
        print("Disconnected.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Take a screenshot for debugging if it fails
        browser.save_screenshot("error_debug.png")
    finally:
        browser.quit()
        if error:
            # exit code in case of error
            sys.exit(1)


if __name__ == '__main__':
    run_declaration()