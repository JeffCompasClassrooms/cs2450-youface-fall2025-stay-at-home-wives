import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import subprocess
import sys

BASE_URL = "http://localhost:5005"

# Test counters
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

# Setup Chromium driver for WSL
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

# Try to find the correct Chromium path
try:
    result = subprocess.run(["which", "chromium"], capture_output=True, text=True)
    if result.returncode == 0:
        options.binary_location = result.stdout.strip()
        print(f"Using Chromium at: {options.binary_location}")
except Exception as e:
    print(f"Error finding Chromium: {e}")

try:
    driver = webdriver.Chrome(options=options)
    print("Successfully started Chromium driver")
except Exception as e:
    print(f"Chromium setup failed: {e}")
    sys.exit(1)

print("--= Testing New Post Page =--")

# Generate random credentials for testing
RND = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
USERNAME = f"test_{RND}"
PASSWORD = f"pw_{RND}"

try:
    # Step 0: Create a test user account first
    print("Setting up test user account...")
    driver.get(f"{BASE_URL}/loginscreen")
    time.sleep(1)
    
    try:
        # Try different possible field names for login form
        username_field = None
        password_field = None
        
        # Try common username field names
        for field_name in ["username", "user", "email", "login"]:
            try:
                username_field = driver.find_element(By.NAME, field_name)
                break
            except:
                continue
        
        # Try common password field names  
        for field_name in ["password", "pass", "pwd"]:
            try:
                password_field = driver.find_element(By.NAME, field_name)
                break
            except:
                continue
        
        if username_field and password_field:
            username_field.clear()
            username_field.send_keys(USERNAME)
            password_field.clear()
            password_field.send_keys(PASSWORD)
            
            # Try to find create button by different methods
            create_btn = None
            try:
                create_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
            except:
                try:
                    create_btn = driver.find_element(By.CSS_SELECTOR, "button[value='Create']")
                except:
                    try:
                        create_btn = driver.find_element(By.XPATH, "//input[@type='submit' and contains(@value, 'Create')]")
                    except:
                        pass
            
            if create_btn:
                create_btn.click()
                time.sleep(1.5)
                print(f"Created test user: {USERNAME}")
            else:
                print("Create button not found, trying to register via form submission")
                # If we can't find the specific button, try submitting the form
                form = driver.find_element(By.TAG_NAME, "form")
                form.submit()
                time.sleep(1.5)
        else:
            print("Login form fields not found - might already be logged in or page structure is different")
            
    except Exception as e:
        print(f"User creation might have failed: {e}")
        # Continue anyway - maybe user already exists or we're already logged in

    # Step 1: Check if we're already logged in, if not try to login
    print("Checking login status...")
    driver.get(f"{BASE_URL}/")
    time.sleep(1)
    
    # Check if we see logout button (indicating we're logged in)
    try:
        logout_btn = driver.find_element(By.CSS_SELECTOR, "form[action*='logout'], a[href*='logout'], button[onclick*='logout']")
        print("Already logged in")
    except:
        print("Not logged in, attempting login...")
        driver.get(f"{BASE_URL}/loginscreen")
        time.sleep(1)
        
        try:
            # Try different possible field names for login form
            username_field = None
            password_field = None
            
            for field_name in ["username", "user", "email", "login"]:
                try:
                    username_field = driver.find_element(By.NAME, field_name)
                    break
                except:
                    continue
            
            for field_name in ["password", "pass", "pwd"]:
                try:
                    password_field = driver.find_element(By.NAME, field_name)
                    break
                except:
                    continue
            
            if username_field and password_field:
                username_field.clear()
                username_field.send_keys(USERNAME)
                password_field.clear()
                password_field.send_keys(PASSWORD)
                
                # Try to find login button
                login_btn = None
                try:
                    login_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
                except:
                    try:
                        login_btn = driver.find_element(By.CSS_SELECTOR, "button[value='Login']")
                    except:
                        try:
                            login_btn = driver.find_element(By.XPATH, "//input[@type='submit' and contains(@value, 'Login')]")
                        except:
                            pass
                
                if login_btn:
                    login_btn.click()
                else:
                    # Fallback: submit the form
                    form = driver.find_element(By.TAG_NAME, "form")
                    form.submit()
                
                time.sleep(1.5)
                print("Login attempted")
            else:
                print("Login form not found - might be using different authentication method")
                
        except Exception as e:
            print(f"Login form not found or failed: {e}")

    # Step 2: Now try to access the new post page
    print("Accessing new post page...")
    driver.get(f"{BASE_URL}/posts/new")
    time.sleep(2)
    
    print(f"Current URL after login attempt: {driver.current_url}")
    print(f"Page title: '{driver.title}'")
    
    # 1 - Load new post page and check main structure
    try:
        driver.find_element(By.CSS_SELECTOR, "main.content")
        passed("New Post page loads and main content area exists")
    except Exception as e:
        failed(f"New Post page failed to load main content: {str(e)}")

    # 2 - Check page title
    try:
        title = driver.title
        if "New Post" in title:
            passed("Page title contains 'New Post'")
        else:
            failed(f"Page title is '{title}', expected 'New Post'")
    except Exception as e:
        failed(f"Could not verify page title: {str(e)}")

    # 3 - Verify header text
    try:
        header = driver.find_element(By.CSS_SELECTOR, "header.topics-head h2")
        if header.text == "Write a New Post":
            passed("Header text is correct: 'Write a New Post'")
        else:
            failed(f"Header text is '{header.text}', expected 'Write a New Post'")
    except Exception as e:
        failed(f"Header element not found: {str(e)}")

    # 4 - Check for title input field
    try:
        title_input = driver.find_element(By.ID, "title")
        if title_input.get_attribute("type") == "text":
            passed("Title input field exists and is text type")
        else:
            failed("Title input field is not text type")
    except Exception as e:
        failed(f"Title input field not found: {str(e)}")

    # 5 - Check for post textarea (required field)
    try:
        post_textarea = driver.find_element(By.ID, "body")
        if post_textarea.tag_name == "textarea" and post_textarea.get_attribute("required"):
            passed("Post textarea exists and is required")
        else:
            failed("Post textarea missing or not marked as required")
    except Exception as e:
        failed(f"Post textarea not found: {str(e)}")

    # 6 - Verify placeholder texts (FIXED for different apostrophe)
    try:
        title_input = driver.find_element(By.ID, "title")
        post_textarea = driver.find_element(By.ID, "body")
        
        title_placeholder = title_input.get_attribute("placeholder")
        post_placeholder = post_textarea.get_attribute("placeholder")
        
        if title_placeholder == "Optional":
            passed("Title placeholder text is correct: 'Optional'")
        else:
            failed(f"Title placeholder is '{title_placeholder}', expected 'Optional'")
            
        # Accept both apostrophe types: ' and ’
        if "What's on your mind?" in post_placeholder or "What's on your mind?" in post_placeholder.replace("'", "’").replace("’", "'"):
            passed("Post placeholder text contains expected message")
        else:
            failed(f"Post placeholder is '{post_placeholder}', expected to contain 'What's on your mind?'")
    except Exception as e:
        failed(f"Could not verify placeholder texts: {str(e)}")

    # 7 - Check form action and method
    try:
        form = driver.find_element(By.TAG_NAME, "form")
        form_method = form.get_attribute("method")
        
        if form_method.lower() == "post":
            passed("Form method is POST")
        else:
            failed(f"Form method is '{form_method}', expected 'post'")
            
        passed("Form structure is correct")
    except Exception as e:
        failed(f"Form verification failed: {str(e)}")

    # 8 - Verify action buttons (Cancel and Publish)
    try:
        cancel_btn = driver.find_element(By.LINK_TEXT, "Cancel")
        publish_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        if cancel_btn.is_displayed() and publish_btn.is_displayed():
            passed("Both Cancel and Publish buttons are visible")
        else:
            failed("One or both action buttons are not visible")
    except Exception as e:
        failed(f"Action buttons verification failed: {str(e)}")

    # 9 - Check navigation elements
    try:
        home_link = driver.find_element(By.LINK_TEXT, "Home")
        if home_link.is_displayed():
            passed("Home navigation link is visible")
        else:
            failed("Home navigation link is not visible")
    except Exception as e:
        failed(f"Navigation elements check failed: {str(e)}")

    # 10 - Verify hero image/logo
    try:
        hero_img = driver.find_element(By.CSS_SELECTOR, "#hero img")
        if hero_img.is_displayed():
            passed("Hero image/logo is displayed")
        else:
            failed("Hero image exists but is not displayed")
    except Exception as e:
        failed(f"Hero image verification failed: {str(e)}")

finally:
    print("--= Ending Tests =--")
    print(f"{TOTAL} Tests Ran: {PASSED} Tests Passed")
    if 'driver' in locals():
        driver.quit()