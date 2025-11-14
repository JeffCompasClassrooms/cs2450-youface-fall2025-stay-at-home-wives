from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

BASE_URL = "http://127.0.0.1:5005/posts/1"
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

tests_run = 0
tests_passed = 0

def test(name, func):
    global tests_run, tests_passed
    try:
        func()
        print(f"[PASSED] - {name}")
        tests_passed += 1
    except Exception as e:
        print(f"[FAILED] - {name} ({e})")
    tests_run += 1

def test_page_loads():
    driver.get(BASE_URL)
    print("Page title is:", driver.title)
    assert len(driver.title) > 0

def test_hero_image_exists():
    driver.get(BASE_URL)
    hero = driver.find_element(By.ID, "slogan")
    assert hero.is_displayed()

def test_footer_exists():
    footer = driver.find_element(By.TAG_NAME, "footer")
    assert "Copyright" in footer.text

def test_post_title_present():
    title = driver.find_element(By.TAG_NAME, "h2")
    assert len(title.text) > 0

def test_post_author_displayed():
    text = driver.find_element(By.CLASS_NAME, "topic-meta").text
    assert "by" in text

def test_comment_section_exists():
    section = driver.find_element(By.TAG_NAME, "section")
    assert "Comments" in section.text

def test_add_comment_textarea_exists():
    textarea = driver.find_element(By.NAME, "body")
    assert textarea.tag_name == "textarea"

def test_submit_comment_button_exists():
    btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    assert btn.is_displayed()

def test_nav_home_link_exists():
    link = driver.find_element(By.LINK_TEXT, "Home")
    assert link.get_attribute("href")

def test_layout_wrapper_exists():
    wrapper = driver.find_element(By.ID, "wrapper")
    assert wrapper is not None

print(f"\nBeginning Tests\n")

test("Page Loads", test_page_loads)
test("Hero Image Exists", test_hero_image_exists)
test("Footer Exists", test_footer_exists)
test("Post Title Present", test_post_title_present)
test("Post Author Displayed", test_post_author_displayed)
test("Comments Section Exists", test_comment_section_exists)
test("Add Comment Textarea Exists", test_add_comment_textarea_exists)
test("Submit Comment Button Exists", test_submit_comment_button_exists)
test("Navigation Home Link Exists", test_nav_home_link_exists)
test("Main Layout Wrapper Exists", test_layout_wrapper_exists)

print(f"\nEnding Tests:\n{tests_run} Tests Ran: {tests_passed} Tests Passed\n")

driver.quit()
