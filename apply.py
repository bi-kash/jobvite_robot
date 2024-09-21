# import packages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import random
import time
from dotenv import load_dotenv
import os
import traceback

# utilizing the `python-dotenv` library to load environment variables from a `.env` file
load_dotenv()
root_dir = os.getcwd()
region = os.environ.get("region")
category = os.environ.get("category")
search_text = os.environ.get("search")
residence_location = os.environ.get("residence_location")
resume_dir = os.environ.get("resume")
first_name = os.environ.get("first_name")
last_name = os.environ.get("last_name")
email = os.environ.get("email")
address = os.environ.get("address")
city = os.environ.get("city")
state = os.environ.get("state")
zip_code = os.environ.get("zip_code")
phone = os.environ.get("phone")
oppurtunity_how = os.environ.get("oppurtunity_how")
expectation_salary = os.environ.get("expectation_salary")
country = os.environ.get("country")


def get_driver():
    """
    The `get_driver` function in Python sets up a Chrome WebDriver with various options like headless
    mode, user agent, proxy, and user data directory.
    :return: The `get_driver` function returns a WebDriver instance for Chrome with specified options
    such as headless mode, user-agent, proxy settings, window maximization, and user data directory.
    """

    chromeOptions = webdriver.ChromeOptions()

    # Headless is faster. If headless is False then it opens a browser and you can see action of web driver. You can try making it False
    chromeOptions.headless = False
    chromeOptions.add_argument("--log-level=3") # suppress console logs
    chromeOptions.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    # installs chrome driver automatically if not present
    s = Service(ChromeDriverManager().install())

    # maximize the window
    chromeOptions.add_argument("start-maximized")

    # read proxy from proxy.txt file and use randomly if available
    
    proxies = open("proxy.txt").read().splitlines()
    if proxies:
        random_proxy = random.choice(proxies)
        # this is how you can set proxy that do not require credentials
        chromeOptions.add_argument(f"--proxy-server={random_proxy}")

    
    
    chromeOptions.add_argument(f"user-data-dir={root_dir}\\Profile")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chromeOptions
    )

    return driver

def random_sleep(min=3, max=6):
    """
    The function `random_sleep` generates a random sleep time between a specified minimum and maximum
    value.
    
    :param min: The `min` parameter in the `random_sleep` function specifies the minimum amount of time,
    in seconds, that the function will sleep for. By default, if no value is provided for `min`, it will
    be set to 3 seconds, defaults to 3 (optional)
    :param max: The `max` parameter in the `random_sleep` function represents the maximum number of
    seconds that the function will sleep for. By default, if no value is provided for `max`, it will
    sleep for a random number of seconds between 3 and 6, defaults to 6 (optional)
    """
    time.sleep(random.randint(min, max))

def search_filter(driver):
    """
    The function `search_filter` performs a search operation on a webpage using specified parameters.
    
    :param driver: The `driver` parameter in the `search_filter` function is typically an instance of a
    web driver, such as Selenium WebDriver, that allows you to interact with a web browser in an
    automated way. You can use this driver to perform actions like finding elements on a webpage,
    clicking buttons, entering text
    """
    try:
        random_sleep()
        driver.find_element(By.XPATH, f"//option[@value='{region}']").click()
        driver.find_element(By.XPATH, f"//option[@value='{category}']").click()
        driver.find_element(By.ID, "jv-search-keyword").send_keys(search_text)
        driver.find_element(By.XPATH, "//button[text()='Search']").click()
        random_sleep()

    except Exception as e:
        print("Error while searching for jobs")
        print("current url: ", driver.current_url)
        print(traceback.format_exc())

def get_valid_jobs(driver):
    """
    The function `get_valid_jobs` retrieves links to job listings that match a specified search text on
    a webpage using Selenium in Python.
    
    :param driver: The `driver` parameter in the `get_valid_jobs` function is typically an instance of a
    web driver, such as Selenium WebDriver, that allows you to interact with a web page in a browser.
    You can use this driver to find elements on the page and perform actions like clicking links or
    buttons
    :return: A list of valid job links that match the search text provided.
    """
    valid_jobs = []
    for element in driver.find_elements(By.CLASS_NAME, 'jv-job-list-name'):
        job = element.text
        if job.lower() == search_text.lower():
            link = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            valid_jobs.append(link)
    return valid_jobs


def apply(driver, valid_jobs):
    """
    The function `apply` automates the job application process by filling out a form and uploading a
    resume for each valid job URL provided.
    
    :param driver: The `driver` parameter in the `apply` function is typically an instance of a
    WebDriver, which is used to automate interactions with a web browser. It allows you to navigate to
    web pages, interact with elements on the page, and perform various actions like clicking buttons,
    filling out forms, and more
    :param valid_jobs: The `valid_jobs` parameter in the `apply` function is a list of job URLs that the
    `driver` will navigate to and apply for. Each URL in the list represents a valid job opportunity
    that the script will attempt to apply for
    """
    for valid_job in valid_jobs:
        try:
            driver.get(valid_job)

            driver.find_element(By.CLASS_NAME, "jv-button-apply").click() # click on apply button

            if driver.find_elements(By.XPATH, f"//option[text()='{residence_location}']"):
                driver.find_element(By.XPATH, f"//option[text()='{residence_location}']").click() # select residence location
            else:
                driver.find_elements(By.TAG_NAME, 'option')[-1].click() # if residence location not found select other

            random_sleep()
            driver.find_element(By.XPATH, "//button[@type='submit']").click() # click on I accept button to accept terms and conditions

            driver.find_element(By.XPATH, "//button[@attachment-label='Resume']").click() # click on upload resume button
            random_sleep()
            file_upload = driver.find_element(By.XPATH, "//div[@ng-show='visible.fileUpload']").find_element(By.ID, 'file-input-0')

            file_upload.send_keys(f'{root_dir}/{resume_dir}') # upload resume with dir mentioned in .env file

            
            WebDriverWait(driver, 20).until(lambda x: x.find_element(By.XPATH, "//span[@class='jv-spinner ng-hide']")) # wait until upload is complete

            # fill the form

            # first name input
            first_name_field = driver.find_element(By.XPATH, "//input[@autocomplete='given-name']")
            first_name_field.clear()
            first_name_field.send_keys(first_name)

            # last name input
            last_name_field = driver.find_element(By.XPATH, "//input[@autocomplete='family-name']")
            last_name_field.clear()
            last_name_field.send_keys(last_name)

            # email input
            email_field = driver.find_element(By.XPATH, "//input[@autocomplete='email']")
            email_field.clear()
            email_field.send_keys(email)

            # address input
            address_field = driver.find_element(By.XPATH, "//input[@autocomplete='address-line1']")
            address_field.clear()
            address_field.send_keys(address)

            # city input
            city_field = driver.find_element(By.XPATH, "//input[@autocomplete='address-level2']")
            city_field.clear()
            city_field.send_keys(city)

            # state input
            state_field_select = driver.find_element(By.XPATH, "//select[@autocomplete='address-level1']")
            state_fields = state_field_select.find_elements(By.XPATH, f"//option[@label='{state}']")
            if state_fields:
                state_fields[0].click()
            else:
                state_field_select.find_element(By.XPATH, "//option[@label='Not Applicable']").click() # if state not found select Not Applicable


            # country input
            driver.find_element(By.XPATH, f"//option[@label='{country}']").click()

            # zip code input
            zip_code_field = driver.find_element(By.XPATH, "//input[@autocomplete='postal-code']")
            zip_code_field.clear()
            zip_code_field.send_keys(zip_code)

            # phone input
            phone_field = driver.find_element(By.XPATH, "//input[@autocomplete='tel']")
            phone_field.clear()
            phone_field.send_keys(phone)

            # how did you hear about this oppurtunity input
            driver.find_element(By.XPATH, f"//option[@label='{oppurtunity_how}']").click()
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            random_sleep()
        except Exception:
            
            print(
                f"Error while applying for job {valid_job}"
            )
            print(traceback.format_exc())
            
if __name__ == "__main__":
    driver = get_driver()
    base_url = "https://jobs.jobvite.com/careers/logitech/jobs" 
    driver.get(base_url)

    # search for jobs. It uses filter from .env file
    search_filter(driver)

    # get valid jobs
    valid_jobs = get_valid_jobs(driver)

    # apply for jobs
    apply(driver, valid_jobs)
