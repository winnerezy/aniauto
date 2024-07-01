from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

ublock_extension_path = os.path.abspath('./uBlock0.chromium')

idm_extension_path = r"C:\Users\USER\AppData\Local\Google\Chrome\User Data\Default\Extensions\ngpampappnmepgilojfohadhhmbhlaek\6.42.11_0"

service = Service(executable_path="chromedriver.exe")

options = webdriver.ChromeOptions()

options.add_argument(f'--load-extension={idm_extension_path},{ublock_extension_path}')

driver = webdriver.Chrome(service=service, options=options)


url = 'https://animepahe.ru'

driver.get(url)

try:

    search_bar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'input-search')]"))
    )

    search_bar.click()

    search = input('What anime are you looking for today ?\n')

    search_bar.send_keys(search)

    anime_search = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(@data-index, '0')]"))
    )

    anime_search.click()

    new_episode = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Watch')]"))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", new_episode)

    new_episode_number = new_episode.text.replace('Watch - ', '').replace('Online', '')

    episode_numbers = input(f'Latest episode is {new_episode_number} \n What episodes (e.g 1,2,3,4,5)  ?\n').split(',')

    quality = input('What quality ? (e.g 360, 720, 1080)\n')

    for episode_number in episode_numbers:
        episode_number = episode_number.strip()

        play_button_xpath = f"//a[contains(text(), 'Watch  - {episode_number} Online')]"

        # look through all the pages for the episodes

        while True:
            try:
                play_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, play_button_xpath)))
                break
            except:
                next_page = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'page-link next-page')]")))
                driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
                time.sleep(1)
                next_page.click()
                time.sleep(1)
            

        driver.execute_script("arguments[0].scrollIntoView(true);", play_button)

        time.sleep(3)

        play_button.click()

        download_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'downloadMenu'))
        )

        download_menu.click()

        download_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(),'{quality}p')]"))
        )

        download_item.click()

        anime_url = download_item.get_attribute('href')

        driver.get(anime_url)

        continue_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn-secondary btn-block redirect')]"))
        )

        time.sleep(10)

        continue_btn.click()

        download_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'button is-uppercase is-success is-fullwidth')]"))
        )
        
        time.sleep(3)

        download_btn.click()

        print(f'Downloading episode {episode_number}')

        # i had to use 3 drive.back() to redirect back to the anime episodes page
        time.sleep(2)

        driver.back()

        time.sleep(2)

        driver.back()

        time.sleep(2)

        driver.back()

        time.sleep(2)

    print('All download started!')
except TimeoutError:
    print('Time out error')

except Exception as e:
    print(f"An error occurred: {e}")

finally: 
    driver.quit()
