#!/usr/bin/env python 

# ref :  https://www.scrapingbee.com/blog/selenium-python/


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time
import json
import os

_config_filename = 'settings.json'  

def get_driver(driver="chrome"):

    match driver:
        case "firefox":
            options = FirefoxOptions()
            options.headless = True
            options.add_argument("--window-size=1920,1200")
            options.add_argument('ignore-certificate-errors')
            service = FirefoxService(executable_path=GeckoDriverManager().install())
            browser = webdriver.Firefox(options=options, service=service)
        case "chrome":
            options = ChromeOptions()
            options.headless = True
            options.add_argument("--window-size=1920,1200")
            options.add_argument('ignore-certificate-errors')
            service = ChromeService(executable_path=ChromeDriverManager().install())
            browser = webdriver.Chrome(options=options, service=service)
        case _:
            browser = None

    return browser

if __name__ == '__main__':

    # Get configuration from json file
    config = json.loads(open(_config_filename).read())

    if "browser" in config.keys() :
        browser = get_driver(driver=config["browser"])
    else:
        print("ERROR: You have to define a browser in the settings.json file")
        os.exit(1)

    if "website_url" in config.keys():
        browser.get(config["website_url"])
    else:
        print("ERROR: You have to define website_url in settings.json file")
        os.exit(1)

    print("Etemptation Authentication")
    if "username" in config.keys() and "password" in config.keys():
        username = browser.find_element(By.ID, "USERID").send_keys(config["username"])
        password = browser.find_element(By.ID, "XXX_PASSWORD").send_keys(config["password"])
        submit = browser.find_element(By.ID, "connect").click()
    else:
        print("ERROR: You have to define username and password in settings.json file")
        os.exit(1)

    try:
        logout_button = browser.find_element(By.ID, "disconnect")
        print("Successfully logged in to Etemptation")
    except:
        print("Incorrect login/password")

    print("Make a declaration for lunch ticket")
    menu = browser.find_element(By.LINK_TEXT, 'Self service').click()
    time.sleep(1)
    ticket_repas = browser.find_element(By.PARTIAL_LINK_TEXT, "Demande de Titre Repas").click()
    time.sleep(1)
    bouton_demande = browser.find_element(By.XPATH, "//input[@value='Nouvelle demande']").click()
    time.sleep(1)

    form_motif = browser.find_element(By.ID, "for/MOTIF").send_keys("ZTCKREST")
    
    form_nombre = browser.find_element(By.ID, "VALDEB_N_label").click()
    form_valeur = browser.find_element(By.ID, "for/MOTIDUR").send_keys("1.00")
    time.sleep(1)


    bouton_valider = browser.find_element(By.ID, "_MODAL_BTNA").click()
    time.sleep(1)

    validation_message = "Votre déclaration a été prise en compte"
    error_message = "Solde insuffisant pour ce motif"
    error = False

    validation = browser.find_element(By.ID, "modale_content")
    if validation_message in validation.text:
        print("Successfully declared")
    else:
        if error_message in validation.text:
            print("Couldn't declare: ", error_message)
            error = True

    try:
        validation = browser.find_element(By.ID, "modale_content")
        if validation_message in validation.text:
            print("Successfully declared")
        else:
            if error_message in validation.text:
                print("Couldn't declare: ", error_message)
                error = True
    except:
        print("Couldn't ask for lunch ticket")

    print("Closing message pop up")
    logout_button = browser.find_element(By.ID, "_MODALMSG_BTNA").click()

    if error:
        print('Closing declaration pop up: Canceling')
        logout_button = browser.find_element(By.ID, "_MODAL_BTNB").click()


    print("Logout")
    logout_button = browser.find_element(By.ID, "disconnect").click()
    print("done")

    browser.quit()