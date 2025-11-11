import time
import random
import string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://127.0.0.1:5005"

RND = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
USERNAME = f"test_{RND}"
PASSWORD = f"pw_{RND}"

TOTAL = 0
PASSED = 0

def passed(msg):
    global TOTAL, PASSED
    TOTAL += 1
    PASSED += 1
    print(f"[PASSED] - {msg}")

def failed(msg):
    global TOTAL
    TOTAL += 1
    print(f"[FAILED] - {msg}")

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

print("--= Beginning Tests =--")

try:
    #1-load index
    driver.get(f"{BASE_URL}/")
    time.sleep(1)
    try:
        driver.find_element(By.CSS_SELECTOR, "main")
        passed("Index loads and <main> exists")
    except Exception:
        failed("Index failed to load <main>")

    #2-sidebar-login visible when logged out
    try:
        driver.find_element(By.CSS_SELECTOR, "#login a.btn.small")
        passed("Login button visible when logged out")
    except Exception:
        failed("Login button missing when logged out")

    #3-login to post visible when logged out
    try:
        driver.find_element(By.LINK_TEXT, "Login to post")
        passed("Login-to-post button visible when logged out")
    except Exception:
        failed("Login-to-post button missing when logged out")

    #4-loginscreen shows uname/pass inputs
    driver.get(f"{BASE_URL}/loginscreen")
    time.sleep(1)
    try:
        driver.find_element(By.NAME, "username")
        driver.find_element(By.NAME, "password")
        passed("Login screen shows username + password inputs")
    except Exception:
        failed("Login screen missing username/password inputs")

    #5-loginscreen shows login/create/delete buttons
    try:
        driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Delete']")
        passed("Found Login, Create, and Delete buttons")
    except Exception:
        failed("Missing one or more of Login/Create/Delete buttons")

    #6-user creation works and redirects back to indedx
    try:
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys(USERNAME)
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']").click()
        time.sleep(1.5)
        if "loginscreen" not in driver.current_url:
            passed("User creation succeeded and redirected")
        else:
            failed("User creation did not redirect")
    except Exception:
        failed("User creation failed")

    #7-logout button visible when logged in
    try:
        driver.find_element(By.CSS_SELECTOR, "form[action='/logout'] button.btn.small")
        passed("Logout button visible after login")
    except Exception:
        failed("Logout button not visible after login")

    #8-new post button visible when logged in
    try:
        driver.find_element(By.LINK_TEXT, "New Post")
        passed("New Post button visible when logged in")
    except Exception:
        failed("New Post button missing when logged in")

    #9-hero image 'logo' is displayed
    try:
        driver.find_element(By.CSS_SELECTOR, "#hero img")
        passed("Hero image is displayed and visible")
    except Exception:
        failed("Hero image was not found")

    #10-home button visible in navigation
    try:
        driver.find_element(By.LINK_TEXT, "Home")
        passed("Home button visible in navigation")
    except Exception:
        failed("Home button not visible in navigation")

finally:
    print("--= Ending Tests =--")
    print(f"{TOTAL} Tests Ran: {PASSED} Tests Passed")
    driver.quit()
