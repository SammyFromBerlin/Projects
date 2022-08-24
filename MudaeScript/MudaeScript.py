import os,threading
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys
from time import sleep
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup for login and start
PATH = "C:\Program Files (x86)\chromedriver.exe" 
email = os.getenv("NAME")
pw = os.getenv("PW")


def scroll_down():
    threading.Timer(5.0, scroll_down())
    last = driver.find_elements_by_xpath("//li")[-1]
    driver.execute_script("return arguments[0].scrollIntoView();", last)

# checks if current characters in list are worth reacting
def check_for_first_rate_characters(current_list, rate_of_character):
    for elem in current_list:
        if (elem in top_characters) or (int(rate_of_character) >= 900):
            elem_info = elem.find_element_by_xpath(".//ancestor::li")
            driver.execute_script("return arguments[0].scrollIntoView();",elem_info)
            sleep(0.5)
            elem_info.click()
            sleep(0.5)
            emoji_button = elem_info.find_element_by_xpath("./div/div[3]//div[@class='button-3bklZh']")
            sleep(0.5)
            emoji_button.click()
            sleep(0.5)
            driver.find_element_by_class_name("input-2FSSDe").send_keys("moon")
            driver.find_element_by_class_name("input-2FSSDe").send_keys(Keys.ENTER)

# roll cards hourly , if extraordinary => check_for_first_rate_characters()
def roll_cards():
    threading.Timer(3600.0, roll_cards()).start()
    card_list = []
    current_lenght_of_cards = driver.find_elements_by_xpath("//div[@class='grid-1aWVsE']/div/span")

    # roll characters max times (non pro-version:10)
    for number in range(10):
        try:
            text_field = driver.find_element_by_xpath("//main/form/div/div/div/div[1]/div/div[3]/div[2]/div")
            sleep(2)
            text_field.send_keys("$ma")
            text_field.send_keys(Keys.ENTER)

            character_card_info = driver.find_elements_by_xpath("//div[@class='grid-1aWVsE']/div/span")[-1]
            sleep(1)
            new_lenght_of_cards = driver.find_elements_by_xpath("//div[@class='grid-1aWVsE']/div/span")

            # check if character appeared
            if len(current_lenght_of_cards) == len(new_lenght_of_cards):
                break

            driver.execute_script("return arguments[0].scrollIntoView();", character_card_info)
            last_character = character_card_info.find_element_by_xpath(".//ancestor::li")
            kakera = last_character.find_element_by_tag_name("strong")
            kakera_of_character = kakera.text
            character_card_name = character_card_info.text
            card_list.append(character_card_name)
            check_for_first_rate_characters(card_list, kakera_of_character)
            card_list = []

        except Exception:
            break

# snipes other people cards if they are currently rolling     
def snipe_characters_from_players(list):
    for character in list:
        #move to character and perfom action
        if character.text in top_characters and character.text != '':
            snipe_current_last_character = character.find_element_by_xpath(".//ancestor::li")
            sleep(1)
            ActionChains(driver).move_to_element(snipe_current_last_character).perform()
            character.click()
            character_react_button = snipe_current_last_character.find_element_by_xpath(
                "./div/div[3]/div[@class='buttons-3dF5Kd container-2gUZhU isHeader-2bbX-L']")
            sleep(1)

            tmp = character_react_button.find_element_by_xpath("./div/div[@class='button-3bklZh']")
            tmp.click()
            
            sleep(1)
            driver.find_element_by_class_name("input-2FSSDe")
            driver.find_element_by_class_name("input-2FSSDe").send_keys(Keys.ENTER)

# snipe checking recent rolled characters
def snipe_cards():
    threading.Timer(5.0, snipe_cards).start()
    while True:
        current_characters_to_snipe = driver.find_elements_by_xpath("//div[@class='grid-1aWVsE']/div/span")
        snipe_list = current_characters_to_snipe[-5:]
        snipe_characters_from_players(snipe_list)
        break

character_list = open("MudaeScript\MudaeTopChars.txt").readlines()
top_characters = list(map(lambda x:x.strip(), character_list))

load_dotenv("Data.env")
driver = webdriver.Chrome(PATH)
driver.get("https://www.discord.com")

sleep(2)

try:
    login_text_elem = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div/a[contains(text(), 'Login')]")))
    login_text_elem.click()
except NoSuchElementException:
    print("Not Found")

# fullscreen optional
driver.maximize_window()
sleep(1)

# login into Discord (Webbrowser)
driver.find_element_by_xpath("//input[contains(@name, 'email')]").send_keys(email)
driver.find_element_by_xpath("//input[contains(@name, 'password')]").send_keys(pw)
driver.find_element_by_xpath("//div[contains(text(), 'Login')]").click()
sleep(2)

# enter Server
try:
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,"//div[@data-dnd-name ='Konohagakure']")))
    element.click()
except NoSuchElementException:
    print("Not Found")

sleep(1)

# if ads from Discord exists
try:
    driver.find_element_by_xpath("//div[contains(text(),'Got it')]").click()
except Exception:
    pass

sleep(2)
driver.find_element_by_xpath("//div[@data-dnd-name ='mudae-games']").click()
sleep(2)

scroll_down()
sleep(1)
roll_cards()
snipe_cards()

# driver.quit()
