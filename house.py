from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

with open("form_data.txt", "r") as file:
    data = {}
    # Read each line in the file
    for line in file:
        # Split the line into key and value
        key, value = line.strip().split(":")
        # Store the key-value pair in the dictionary
        data[key] = value
    
def retrying_find_click(by):
    result = False
    attempts = 0
    while attempts < 2:
        try:
            driver.find_element(by).click()
            result = True
            break
        except StaleElementReferenceException:
            pass
        attempts += 1
    return result

def accept_cookies():
    try:
        wait = WebDriverWait(driver, 5)
        form = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="cdk-overlay-0"]/div[2]/div[2]/div[2]/button[2]')))
        terms_popup = driver.find_element(By.XPATH, '//*[@id="cdk-overlay-0"]')
        accept_button = driver.find_element(By.XPATH, '//*[@id="cdk-overlay-0"]/div[2]/div[2]/div[2]/button[2]')
        accept_button.click()
    except:
        pass

alreadyApplied = []

while True:
    # Initialize web driver
    driver = webdriver.Chrome()
    #driver2 = webdriver.Chrome()
    # Navigate to website
    #driver.get("https://web.archive.org/web/20230117111159/https://www.wbm.de/wohnungen-berlin/angebote-wbm/")
    driver.get("https://www.wbm.de/wohnungen-berlin/angebote-wbm/")

    accept_cookies()

    # Find all posts
    posts = driver.find_elements(By.XPATH, "//a[@class='btn sign'][@title='Details']")
    
    odd = False
    # Iterate through each post and apply
    
    for post in posts:
        if odd == False:
                posts.remove(post)
                continue
        odd = True

    addressesHolder = driver.find_elements(By.CLASS_NAME, 'address')
    
    addresses = []
    
    for address in addressesHolder:
        addresses.append(address.text)
    
    for i in range(len(addresses)):
        if addresses[i] in alreadyApplied:
            posts.remove(posts[i])
            print("Already applied to " + addresses[i])
        else:
            alreadyApplied.append(addresses[i])
            print("Applying for: " + addresses[i])

    #i = posts.count()


    #loop as posts length
    #if posts adress is in adress-array 
    # remove the post

    #i = 0
    for post in posts:
        
        accept_cookies()

        post.click()
        #try:
        #    ActionChains(driver).scroll_to_element(post).perform()
        #except:
        #    post = posts[i]
        #    ActionChains(driver).scroll_to_element(post).perform()
        #   i = i + 1

        # Click on post
        #post.click()
        #retrying_find_click(post)
        accept_cookies()

        # Wait for application form to load
        #wait = WebDriverWait(driver, 10)
        wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
        form = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="c722"]/div/div/form')))

        # Fill out form
        name_field = driver.find_element(By.ID, 'powermail_field_name')
        name_field.send_keys(data['Name'])

        surname_field = driver.find_element(By.ID, 'powermail_field_vorname')
        surname_field.send_keys(data['Vorname'])

        strasse_field = driver.find_element(By.ID, 'powermail_field_strasse')
        strasse_field.send_keys(data['Strasse'])

        plz_field = driver.find_element(By.ID, 'powermail_field_plz')
        plz_field.send_keys(data['Plz'])

        ort_field = driver.find_element(By.ID, 'powermail_field_ort')
        ort_field.send_keys(data['Ort'])

        email_field = driver.find_element(By.ID, 'powermail_field_e_mail')
        email_field.send_keys(data['Email'])

        telefon_field = driver.find_element(By.ID, 'powermail_field_telefon')
        telefon_field.send_keys(data['Phone'])

        checkbox_field = driver.find_element(By.ID, 'powermail_field_datenschutzhinweis_1')
        driver.execute_script("arguments[0].click();", checkbox_field)
        # Submit form
        submit_button = driver.find_element(By.XPATH, '//*[@id="c722"]/div/div/form/div[2]/div[15]/div/div/button')
        submit_button.click()

        # Go back to job listings
        driver.back()
        accept_cookies()
        driver.back()
        accept_cookies()


    # Close browser
    driver.quit()

