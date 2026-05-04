#!/usr/bin/env python 

# ref :  https://www.scrapingbee.com/blog/selenium-python/


import os
import time

from selenium import webdriver
from selenium.webdriver import Keys
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
        browser.find_element(By.ID, "passwordLogin").send_keys(config["password"])
        browser.find_element(By.ID, "connectBtn").click()

        time.sleep(1)
        disconnect = browser.find_element(By.ID, "disconnect")
        print("Successfully logged in.")

        # Navigate to Lunch Tickets
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Self service'))).click()
        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Demande de Titre Repas"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Nouvelle demande']"))).click()

        # Fill Form
        wait.until(EC.presence_of_element_located((By.ID, "for/MOTIF"))).send_keys("ZTCKREST",Keys.RETURN)
        # browser.find_element(By.ID, "VALDEB_N_label").click()
        # browser.find_element(By.ID, "for/MOTIDUR").send_keys("1.00")
        browser.find_element(By.ID, "_MODAL_BTNA").click()

        # Validation Logic
        modal = wait.until(EC.visibility_of_element_located((By.ID, "modale_content")))
        content = modal.text
        error = False

        if "Votre déclaration a été prise en compte" in content:
            print("Success: Declaration submitted.")
        elif "Solde insuffisant" in content:
            print(f"Error: {content}.")
            error = True

        browser.find_element(By.ID, "_MODALMSG_BTNA").click()  # Cancel
        if error:
            wait.until(EC.element_to_be_clickable((By.ID, "_MODAL_BTNB"))).click()

        time.sleep(0.5)
        disconnect.click()
        print("Done.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Take a screenshot for debugging if it fails
        browser.save_screenshot("error_debug.png")
    finally:
        browser.quit()


if __name__ == '__main__':
    run_declaration()