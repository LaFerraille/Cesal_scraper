import time
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime

options = Options()
options.add_argument("--window-size=1920,1200")
options.add_argument("--incognito")
options.add_argument("--headless")

url = "https://logement.cesal-residentiel.fr/espace-resident/cesal_mon_logement_reservation.php"

driver = webdriver.Chrome(options=options)
driver.get(url)

driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-success btn-lg push-20']").click()

email = "raphael.romandferroni@student-cs.fr"
mdp = "Wapiti24!+"

driver.find_element(By.ID, "login-email").send_keys(email)
driver.find_element(By.ID, "login-password").send_keys(mdp)

driver.find_element(By.XPATH, '//*[@id="connexion"]/form/div[4]/div/button').click()
time.sleep(2)

driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-primary']").click()
time.sleep(2)

date = "25/06/2024"

driver.find_element(By.CSS_SELECTOR, "input[class='form-control']").send_keys(date)

driver.find_element(By.TAG_NAME, "div").click()

driver.find_element(By.XPATH, '//*[@id="selection_creneau"]/div[1]/div[2]/span/span[1]/span/span[2]' ).click()
dates = driver.find_elements(By.CSS_SELECTOR, "li[class^='select2-results__option']")

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

df.to_csv('results.csv',index=False)
    
results = pd.read_csv('results.csv')

for col in results.columns[1:] :
    if 1 in list(results[col]) :
        indice = list(results[col]).index(1)
        
        sender_email = 'raphaelromandferroni@gmail.com'
        sender_password = 'ytossmklcjwgjkyc'
        recipient_email = 'b00786419@essec.edu'

        message = f"Il y a une chambre disponible en {col} a partir du {results['date'][indice]}. Allez depeche toi ma poule !"
        
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, message)
                print("Email sent successfully at {}".format(datetime.now()))
        except Exception as e:
            print(f"Email could not be sent: {str(e)}")
    else : 
        print('No room mate')

print("On est le {}".format(datetime.now()))

driver.quit()