from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import requests
import base64
import random
from undetected_chromedriver import Chrome, ChromeOptions

# Configuration
api_key = ''  # 2Captcha API Key
form_url = 'https://www.usvisascheduling.com/'  # Update with your actual URL
username = ''
password = ''


# Function to simulate scrolling down the page with slight variation
def scroll_down(driver):
    try:
        scroll_amount = random.randint(200, 400)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        print(f"Scrolled down the page by {scroll_amount} pixels")
        time.sleep(random.uniform(0.5, 1.5))  # Random delay after scrolling

    except Exception as e:
        print(f"Error scrolling down the page: {e}")

def check_waiting_room(driver):
    
    try:
        waiting_indicator = (By.XPATH, '//div[@id="image-section"]/img[@alt="processing-image"]')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(waiting_indicator)
        )
        print("Waiting room detected. Waiting to exit...")

        WebDriverWait(driver, 300).until_not(
            EC.presence_of_element_located(waiting_indicator)
        )
        print("Out of waiting room. Proceeding with actions.")
    except Exception:
        print("No waiting room detected. Proceeding with actions.")
    except Exception as e:
        print(f"Error checking/waiting in waiting room: {e}")

def click_reschedule_appointment(driver):
    try:
        time.sleep(5)  # Wait to avoid premature clicks
        reschedule_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="continue_application"]'))

        )

        reschedule_button.click()
        print("Clicked on reschedule appointment button.")

        try:
            cloudfare=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="CdRm7"]/div/label/input')))
            cloudfare.click()
        except Exception as e:
             print(" NOt found or solved automatically")    
        time.sleep(10)
        # Assuming you want to select an option from a dropdown after clicking the button
        select_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="post_select"]'))
        )
        
        option_text = "CHENNAI VAC"
        select = Select(select_element)
        select.select_by_visible_text(option_text)
        print(f"Selected option with text: {option_text}")

    except Exception as e:
        print(f"Error clicking on reschedule appointment button: {e}")

def select_available_date_in_range(driver, start_year, end_year):
    try:
        
        calendar = WebDriverWait(driver, 80).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="datepicker"]')))
        available_dates = []
        rows = calendar.find_elements(By.XPATH, '//*[@id="datepicker"]/div/div[1]/table/thead/tr')
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            for cell in cells:
                if 'background-color: green;' in cell.get_attribute('style') or ' greenday' in cell.get_attribute('class'):
                    available_dates.append(cell)
                    cell.click()
                    
                    time.sleep(3)
                    
                    radio=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="53282f26-3639-ef11-a316-001dd80637a9"]')))
                    radio.click()
                    return True
        return False
    except Exception as e:
        print(f"Date selection error: {e}")
        return False

def solve_captcha(api_key, base64_image):
    captcha_data = {
        'key': api_key,
        'method': 'base64',
        'body': base64_image,
        'json': 1
    }
    response = requests.post('http://2captcha.com/in.php', data=captcha_data)
    captcha_id = response.json().get('request')

    result_url = f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1'
    while True:
        time.sleep(5)  
        result = requests.get(result_url).json()
        if result.get('status') == 1:
            return result.get('request')
        print("Waiting for captcha solution...")

def get_captcha_base64(driver, captcha_img_element):
    return driver.execute_script("""
        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        var img = arguments[0];
        canvas.width = img.width;
        canvas.height = img.height;
        context.drawImage(img, 0, 0);
        return canvas.toDataURL('image/png').split(',')[1];
    """, captcha_img_element)

def process_captcha_and_login(driver, retries=10):
    check_waiting_room(driver)

    for attempt in range(retries):
        try:

            # Wait for the login form elements to be present
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'signInName')))
            username_field = driver.find_element(By.ID, 'signInName')
            username_field.clear()
            username_field.send_keys(username)
            
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'password')))
            password_field = driver.find_element(By.ID, 'password')
            password_field.clear()
            password_field.send_keys(password)

            try:
                scroll_down(driver)
                # Check for the CAPTCHA and solve it if present
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'captchaImage')))
                captcha_img = driver.find_element(By.ID, 'captchaImage')
                base64_image = get_captcha_base64(driver, captcha_img)
                captcha_solution = solve_captcha(api_key, base64_image)
                captcha_field = driver.find_element(By.ID, 'extension_atlasCaptchaResponse')
                captcha_field.clear()
                captcha_field.send_keys(captcha_solution)
            except Exception as captcha_error:
                print(f"Error solving CAPTCHA: {captcha_error}")
                driver.refresh()
                continue

            # Optionally handle the CAPTCHA token if it exists
            try:
                captcha_token_field = driver.find_element(By.ID, 'extension_atlasCaptchaToken')
                if captcha_token_field.is_displayed():
                    captcha_token_field.clear()
                    captcha_token_field.send_keys('')  # If a token is needed
            except:
                pass
            
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'continue')))
            submit_button = driver.find_element(By.ID, 'continue')
            submit_button.click()

            time.sleep(8)  # Allow time for the page to process the login
            
            # Check for login errors
            try:
                error_element = driver.find_element(By.ID, 'claimVerificationServerError')
                if error_element.is_displayed() and "Validation is not Successful." in error_element.text:
                    print(f"Attempt {attempt + 1} failed: {error_element.text}")
                    driver.refresh()
                    continue
            except:
                pass

            print("Login successful.")
            break  # Exit the retry loop on success

        except Exception as e:
            print(f"An error occurred: {e}")
            driver.refresh()  # Refresh on any errors to retry

    # Answer security questions if prompted
    try:
        # List of possible question element IDs
        question_ids = ['kbq1ReadOnly', 'kbq2aReadOnly', 'kbq2bReadOnly', 'kbq3ReadOnly']
        question_elements = []

        # Find all available question elements
        for qid in question_ids:
            try:
                question_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, qid)))
                question_elements.append(question_element)
                if len(question_elements) >= 2:  # We need only two questions
                    break
            except:
                continue  # Try the next ID

        # Ensure we have exactly two question elements
        if (len(question_elements) != 2):
            print(f"Expected 2 questions but found {len(question_elements)}")
            return

        # Extract the questions and determine answers
        question1 = question_elements[0].text
        question2 = question_elements[1].text

        print(f"Security Question 1: {question1}")
        print(f"Security Question 2: {question2}")

        # Set answers based on keyword checks
        answer_mapping = {
            "born": "MUMBAI",
            "childhood ": "SACHIN",
            "food": "APPLE",
            "PAX NAME": "MANSI PRIYANKBHAI PATEL X 2",
            "country": "norway"  # Add more keyword-answer pairs as needed
        }

        # Function to determine the answer based on the question content
        def determine_answer(question):
            for keyword, answer in answer_mapping.items():
                if keyword in question.lower():
                    return answer
            return "unknown"  # Default answer if no keyword matches

        # Determine the answers
        answer1 = determine_answer(question1)
        answer2 = determine_answer(question2)

        # Determine response field IDs based on question element IDs
        response_fields = {
            'kbq1ReadOnly': 'kba1_response',
            'kbq2aReadOnly': 'kba2_response',
            'kbq2bReadOnly': 'kba2_response',
            'kbq3ReadOnly': 'kba3_response'
        }

        # Fill in the answers
        response1_field = driver.find_element(By.ID, response_fields[question_elements[0].get_attribute('id')])
        response1_field.clear()
        response1_field.send_keys(answer1)

        response2_field = driver.find_element(By.ID, response_fields[question_elements[1].get_attribute('id')])
        response2_field.clear()
        response2_field.send_keys(answer2)

        # Submit the security questions
        submit_button = driver.find_element(By.ID, 'continue')
        time.sleep(10)
         
        submit_button.click()
        print("Security questions answered and form submitted successfully.")
        check_waiting_room(driver)
        
    except Exception as e:
        print(f"An error occurred while answering security questions: {e}")

chrome_options = ChromeOptions()
chrome_options.add_argument(r"--user-data-dir=C:\\Users\\Toshiba\\AppData\\Local\\Google\\Chrome\\User Data")
chrome_options.add_argument(r"--profile-directory=Profile 1")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')

# Create a new instance of the undetected Chrome driver with the specified options
driver = Chrome(options=chrome_options)

driver.get(form_url)

process_captcha_and_login(driver)

# Proceed to click the reschedule appointment button
click_reschedule_appointment(driver)
select_available_date_in_range(driver, 2024, 2025)

# Allow some time for any post-click actions
time.sleep(1000)
