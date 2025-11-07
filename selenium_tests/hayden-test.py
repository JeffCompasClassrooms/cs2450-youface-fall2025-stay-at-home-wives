from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Don't specify chromedriver path!
driver = webdriver.Chrome(options=options)

try:
    driver.get("http://localhost:8000")
    #time.sleep(2)

    print("--= Beginning Tests - Hayden Jones =--")

    logo = driver.find_element(By.ID, "slogan")
    if logo:
        print("[PASSED] - Logo image Exists.")
    else:
        print("[FAILED] - Logo image not found.")

    login_button = driver.find_element(By.ID, "login")
    if login_button:
        print("[PASSED] - Login button exists.")
    else:
        print("[FAILED] - Login button not found.")

    ship_background_image = driver.find_element(By.ID, "login").value_of_css_property("background-image")
    if ship_background_image == "assets/sea-ship.png":
        print("[PASSED] - Correct background image.")
    else:
        print("[FAILED] - Incorrect background image or image not found.")

    nav = driver.find_element("tag name", "nav")
    if login_button:
        print("[PASSED] - Nav sidebar exists.")
    else:
        print("[FAILED] - Nav sidebar not found.")

    nav_text_color = driver.find_element("tag name", "nav").value_of_css_property("color")
    if nav_text_color == "rgba(255, 255, 255, 1)":
        print("[PASSED] - Correct Nav text color.")
    else:
        print("[FAILED] - Incorrect Nav text color.")

    sidebar_width = driver.find_element("tag name", "nav").value_of_css_property("width")
    if sidebar_width == "217":
        print("[PASSED] - Correct Nav width.")
    else:
        print("[FAILED] - Incorrect Nav width.")

    font_family = driver.find_element("tag name", "body").value_of_css_property("font-family")
    if font_family.__contains__("Bona Nova SC"):
        print("[PASSED] - Bona Nova SC font family present.")
    else:
        print("[FAILED] - Bona Nova SC font family not present.")

    copyright_statement = driver.find_element("tag name", "nav").text
    if copyright_statement == "Copyright © 2025 stay@homewives":
        print("[PASSED] - Correct copyright statment.")
    else:
        print("[FAILED] - Incorrect copyright statement.")

    new_post_button = driver.find_elements("class name", "btn small")[1]
    if new_post_button:
        print("[PASSED] - New post button exists.")
    else:
        print("[FAILED] - New post button not found.")

    new_post_button_href = new_post_button.get_property("href")
    if new_post_button_href == "/posts/new":
        print("[PASSED] - Home link exists.")
    else:
        print("[FAILED] - Home link not found.")

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
