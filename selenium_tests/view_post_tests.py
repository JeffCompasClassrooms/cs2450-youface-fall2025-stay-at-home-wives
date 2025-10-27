import random
import string
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://localhost:5005"

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

# Don't specify chromedriver path!
driver = webdriver.Chrome(options=options)

RND = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
USERNAME = f"test_{RND}"
PASSWORD = f"pw_{RND}"

try:
    # Create user
    driver.get(f"{BASE_URL}/loginscreen")
    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create User']").click()
    time.sleep(1)

    # Login
    driver.get(f"{BASE_URL}/loginscreen")
    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']").click()
    time.sleep(1)

    print("--= Beginning Tests - View Post Page =--")

    # Create a post
    driver.get(f"{BASE_URL}/posts/new")
    post_title = f"Title-{RND}"
    post_text = f"This is the post text for test user {USERNAME}."
    driver.find_element(By.NAME, "title").send_keys(post_title)
    driver.find_element(By.NAME, "text").send_keys(post_text)
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(1)

    # Navigate to the post
    driver.find_element(By.LINK_TEXT, post_title).click()
    time.sleep(1)

    # --- Start of Tests ---

    # Test 1: Post title is correct
    try:
        title_element = driver.find_element(By.TAG_NAME, "h1")
        if title_element.text == post_title:
            passed("Post title is displayed correctly.")
        else:
            failed(f"Post title is incorrect. Expected '{post_title}', got '{title_element.text}'.")
    except Exception:
        failed("Could not find post title element (h1).")

    # Test 2: Post author is correct
    try:
        author_element = driver.find_element(By.XPATH, f"//*[contains(text(), 'by {USERNAME}')]")
        passed("Post author is displayed correctly.")
    except Exception:
        failed("Could not find post author element.")

    # Test 3: Post body is correct
    try:
        body_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{post_text}')]")
        passed("Post body is displayed correctly.")
    except Exception:
        failed("Could not find post body element.")

    # Test 4: Comment form exists
    try:
        driver.find_element(By.TAG_NAME, "form")
        passed("Comment form exists.")
    except Exception:
        failed("Comment form does not exist.")
        
    # Test 5: Comment textarea exists
    try:
        driver.find_element(By.NAME, "body")
        passed("Comment textarea exists.")
    except Exception:
        failed("Comment textarea does not exist.")

    # Test 6: Comment submit button exists
    try:
        driver.find_element(By.CSS_SELECTOR, "form input[type='submit']")
        passed("Comment submit button exists.")
    except Exception:
        failed("Comment submit button does not exist.")

    # Add a comment
    comment_text = f"This is a comment from {USERNAME}."
    driver.find_element(By.NAME, "body").send_keys(comment_text)
    driver.find_element(By.CSS_SELECTOR, "form input[type='submit']").click()
    time.sleep(1)

    # Test 7: New comment appears on page
    try:
        driver.find_element(By.XPATH, f"//*[contains(text(), '{comment_text}')]")
        passed("Submitted comment appears on page.")
    except Exception:
        failed("Submitted comment did not appear on page.")

    # Test 8: Comment author is correct
    try:
        driver.find_element(By.XPATH, f"//*[contains(text(), '{USERNAME}:')]")
        passed("Comment author is displayed correctly.")
    except Exception:
        failed("Comment author is not displayed correctly.")

    # Test 9: Back to Feed link exists
    try:
        driver.find_element(By.LINK_TEXT, "Back to Feed")
        passed("'Back to Feed' link exists.")
    except Exception:
        failed("'Back to Feed' link does not exist.")

    # Test 10: Back to Feed link works
    try:
        driver.find_element(By.LINK_TEXT, "Back to Feed").click()
        time.sleep(1)
        if "Feed" in driver.title or driver.current_url == f"{BASE_URL}/":
             passed("'Back to Feed' link navigates to the feed.")
        else:
             failed("'Back to Feed' link does not navigate to the feed.")
    except Exception as e:
        failed(f"'Back to Feed' link test failed: {e}")

finally:
    print("--= Ending Tests =--")
    print(f"{TOTAL} Tests Ran: {PASSED} Tests Passed")
    driver.quit()
