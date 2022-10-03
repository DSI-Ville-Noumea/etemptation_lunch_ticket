#!/usr/bin/env python 

# ref :  https://www.scrapingbee.com/blog/selenium-python/


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

_config_filename = 'settings.json'

_website = "https://etemptation.XXXXXXXXXX/

_username = 'XXXXX'
_password = 'YYYYYYY'

DRIVER_PATH =  '/usr/bin/chromedriver'
prefs = {"CapabilityType.ACCEPT_SSL_CERTS" : "true"}

if __name__ == '__main__':

    options = Options()
    #options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument('ignore-certificate-errors')

    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.get(_website)

    #print(driver.page_source)
    print("Etemptation Authentication")
    username = driver.find_element(By.ID, "USERID").send_keys(_username)
    password = driver.find_element(By.ID, "XXX_PASSWORD").send_keys(_password)
    submit = driver.find_element(By.ID, "connect").click()

    try:
        logout_button = driver.find_element(By.ID, "disconnect")
        print("Successfully logged in to Etemptation")
    except:
        print("Incorrect login/password")

    print("Make a declaration for lunch ticket")
    menu = driver.find_element(By.LINK_TEXT, 'Self service').click()
    time.sleep(1)
    ticket_repas = driver.find_element(By.PARTIAL_LINK_TEXT, "Demande de Titre Repas").click()
    time.sleep(1)
    bouton_demande = driver.find_element(By.XPATH, "//input[@value='Nouvelle demande']").click()
    time.sleep(1)

    form_motif = driver.find_element(By.ID, "for/MOTIF").send_keys("ZTCKREST")
    
    form_nombre = driver.find_element(By.ID, "VALDEB_N_label").click()
    form_valeur = driver.find_element(By.ID, "for/MOTIDUR").send_keys("1.00")
    time.sleep(1)


    bouton_valider = driver.find_element(By.ID, "_MODAL_BTNA").click()
    time.sleep(2)

    validation_message = "Votre déclaration a été prise en compte"
    error_message = "Solde insuffisant pour ce motif"
    error = False

    validation = driver.find_element(By.ID, "modale_content")
    if validation_message in validation.text:
        print("Successfully declared")
    else:
        if error_message in validation.text:
            print("Couldn't declare: ", error_message)
            error = True

    try:
        validation = driver.find_element(By.ID, "modale_content")
        if validation_message in validation.text:
            print("Successfully declared")
        else:
            if error_message in validation.text:
                print("Couldn't declare: ", error_message)
                error = True
    except:
        print("Couldn't ask for lunch ticket")

    print("Closing message pop up")
    logout_button = driver.find_element(By.ID, "_MODALMSG_BTNA").click()

    if error:
        print('Closing declaration pop up: Canceling')
        logout_button = driver.find_element(By.ID, "_MODAL_BTNB").click()


    print("Logout")
    logout_button = driver.find_element(By.ID, "disconnect").click()
    print("done")

    driver.quit()