import argparse
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main(end_date, headless=True):

    cesal_id = os.environ.get("CESAL_ID")
    cesal_password = os.environ.get("CESAL_PASSWORD")
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    recipient_email = os.environ.get("RECIPIENT_EMAIL")

    # Check the date format is correct DD/MM/YYYY
    try:
        datetime.strptime(end_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be DD/MM/YYYY")
    
    # Check the date is in the future
    if datetime.strptime(end_date, '%d/%m/%Y') < datetime.now():
        raise ValueError("The date should be in the future")
    
    # Check the date is not too close
    if datetime.strptime(end_date, '%d/%m/%Y') < datetime.now() + timedelta(days=80):
        raise ValueError("The date should not be less than two months and twenty days in the future")
    
    options = Options()
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--incognito")

    if headless:
        options.add_argument("--headless=new")

    url = "https://logement.cesal-residentiel.fr/espace-resident/cesal_mon_logement_reservation.php"

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-success btn-lg push-20']").click()

    driver.find_element(By.ID, "login-email").send_keys(cesal_id)
    driver.find_element(By.ID, "login-password").send_keys(cesal_password)

    driver.find_element(By.XPATH, '//*[@id="connexion"]/form/div[4]/div/button').click()
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-primary']").click()
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, "input[class='form-control']").send_keys(end_date)

    driver.find_element(By.TAG_NAME, "div").click()

    driver.find_element(By.XPATH, '//*[@id="selection_creneau"]/div[1]/div[2]/span/span[1]/span/span[2]' ).click()
    dates = driver.find_elements(By.CSS_SELECTOR, "li[class^='select2-results__option']")
    print(dates)
    driver.find_element(By.XPATH, '//*[@id="selection_creneau"]/div[1]/div[2]/span/span[1]/span/span[2]').click()

    cols = list(['date','residence_1','residence_2','residence_3','residence_4','residence_5','residence_6'])
    df = pd.DataFrame(columns=cols)

    for i in range(2,len(dates)+1) :
        driver.find_element(By.XPATH, '//*[@id="selection_creneau"]/div[1]/div[2]/span/span[1]/span/span[2]' ).click()
        d = driver.find_element(By.CSS_SELECTOR, "ul[class='select2-results__options'] > li:nth-of-type(" + str(i) + ")")
        date = d.get_attribute('textContent')
        d.click()
        driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-success']").click()
        l = []

        for res,label in zip(driver.find_elements(By.CSS_SELECTOR, "div[id^='residence_'] > h3"),driver.find_elements(By.CSS_SELECTOR, "div[id^='residence_'] > h6")) :
            lab = '0' if label.get_attribute('textContent') == 'Aucun logement disponible' else '1'
            l.append(lab)

        results = {'date':date,'residence_1':l[0],'residence_2':l[1],'residence_3':l[2],'residence_4':l[3],'residence_5':l[4],'residence_6':l[5]}
        new_df = pd.DataFrame(results, index=[0])
        df = pd.concat([df, new_df], ignore_index=True)
        time.sleep(2)

    for col in df.columns[1:] :
        if str(1) in list(df[col]) :
            indice = list(df[col]).index(str(1))
            
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = "Disponibilité d'appartement Cesal"
                        
            body = f"Il y a une chambre disponible en Résidence {str(col).split('_')[-1]} à partir du {df['date'][indice]} pour une date de départ prévue le {end_date}. Allez hurry up avant de te retrouver à la rue !"
            message.attach(MIMEText(body, "plain", "utf-8"))

            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient_email, message.as_string())
                    print("Email sent successfully at {}".format(datetime.now()))
            except Exception as e:
                print(f"Email could not be sent: {str(e)}")
        else : 
            print('Il n\'y a pas de chambre disponible en {}'.format(col))

    print("On est le {}".format(datetime.now()))

    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Cesal for room availabilities.")
    parser.add_argument("--end_date", help="End date of your desired location (should be in format DD/MM/YYYY)", required=True)
    parser.add_argument("--headless", type=bool, default=True, help="Run Chrome in headless mode (default: True). Use --headless False to disable.")

    args = parser.parse_args()
    
    main(args.end_date, args.headless)