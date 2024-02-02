import os, sys
this_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(this_path)

from pathlib import Path
import time
import json
import random
import pyperclip

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from selenium_stealth import stealth

import undetected_chromedriver as uc
# import seleniumwire.undetected_chromedriver as uc


basic_url = 'https://chat.openai.com'
login_url = 'https://chat.openai.com/auth/login/'

class MyDriver:

    def __init__(self, name = "Unknown", headless=True):
        print("_________________________________________________")
        self.current_url = basic_url
        self.name = name

        options = uc.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("--auto-open-devtools-for-tabs")

        self.driver = uc.Chrome(options=options)
        
        stealth(
            self.driver,
            languages = ["en-US", "en"],
            vendor = "Google Inc.",
            platform = "Win32",
            webgl_vendor = "Intel Inc.",
            renderer = "Intel Iris OpenGL Engine",
            fix_hairline = True,
        )

        # Open a new window 
        self.driver.execute_script(f"window.open('', '{basic_url}');") 
        time.sleep(4)
        # Switch to the new window and open new URL 
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(1)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        print("...............................................")


    def turn_off(self):
        self.driver.quit()


    def go_to(self, url_=basic_url, wait_time_=4):
        self.driver.get(url_)
        time.sleep(wait_time_)


    def save_cookie(self, MAIL):
        cookies_subpath = "/Cookies/" + MAIL + ".json"
        cookies_path = this_path + cookies_subpath
        Path(cookies_path).write_text(
            json.dumps(self.driver.get_cookies(), indent=4)
        )
        print("Save success for", self.name)
        return cookies_subpath
    

    def load_cookie(self, cookies_subpath):
        load = False
        cookies_path = this_path + cookies_subpath
        cookies = json.loads(Path(cookies_path).read_text())
        for cookie in cookies:
            try:
                self.driver.add_cookie(cookie)
                load = True
            except:
                continue
        print("Load cookies successfully for", self.name)
        return load
    

    def openai_login(self, NAME, MAIL, PASSWORD, COOKIES):
        res_cookies = ""
        # Try to login with cookies
        load = False
        # if len(COOKIES):
        #     try:
        #         self.go_to(url_=basic_url, wait_time_=4)
        #         self.driver.delete_all_cookies()
        #         load = self.load_cookie(COOKIES)
        #         if load:
        #             self.go_to(url_=basic_url, wait_time_=1)
        #             res_cookies = "Needless"
        #     except Exception as e:
        #         print(self.name, "Error occurred when trying to login with cookies:", e)
        
        if not load:
            try:
                print(NAME + "'s account needs to be logged in with a password.")
                self.go_to(url_=login_url, wait_time_=7)
                login_btn_tag = self.driver.find_element(By.XPATH, "//button[@data-testid='login-button']")
                login_btn_tag.click()
                time.sleep(8)
    
                mail = self.driver.find_element(By.XPATH, "//input[@name='username']")
                mail.send_keys(MAIL)
                time.sleep(2)
                btn = self.driver.find_element(By.XPATH, "//button[@name='action']")
                btn.click()
                time.sleep(2)
    
                password = self.driver.find_element(By.XPATH, "//input[@name='password']")
                password.send_keys(PASSWORD)
                time.sleep(2)

                btn = self.driver.find_elements(By.XPATH, "//button[@name='action']")[-1]
                btn.click()
                time.sleep(2)
                
            except Exception as e:
                print(e)
                pass
            
            res_cookies = self.save_cookie(MAIL=MAIL)
        return res_cookies
    

    def skip_popups(self):
        # We've updated our Terms of Use and Privacy Policy
        try:
            while True:
                time.sleep(5)
                tmp_btn = self.driver.find_elements(By.XPATH, "//button[@class='btn relative btn-primary']")
                if len(tmp_btn) == 2:
                    tmp_btn[-1].click()
                else:
                    break
        except:
            pass
    

    def chat(self, prompt, new_chat_flag, outerHTML_flag):
        def problems_existed():
            over = None
            policy_violated_class_name = "//button[@class='btn relative btn-neutral']"
            policy_violated_btn = self.driver.find_elements(By.XPATH, policy_violated_class_name)
            if len(policy_violated_btn):
                over = "This prompt may violate our content policy."
                policy_violated_btn[-1].click()
                print(f"{self.name} gui prompt vi pham chinh sach cua chatgpt.")
            else:
                alert_class_name = "//div[@class='flex flex-grow flex-col max-w-full']"
                alert = self.driver.find_elements(By.XPATH, alert_class_name)
                if len(alert):
                    lastText = alert[-1].text
                    problems = [
                        "Too many requests",
                        "Something went wrong",
                        "An error occurred",
                        "Network error",
                        "You've reached our limit",
                        "The conversation is too long, please start a new one",
                        "The message you submitted was too long",
                        "account has been deactivated"
                    ]
                    for problem in problems:
                        if problem in lastText:
                            over = lastText
                            break
            return over

        def create_new_chat():
            # self.go_to(url_="https://chat.openai.com/?model=gpt-4", wait_time_=4)
            self.go_to(url_=basic_url, wait_time_=4)


        def send_prompt():
            wait = WebDriverWait(self.driver, 120)
            prompt_split = prompt.split('\n')
            query = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//textarea[@id='prompt-textarea']"))
            )
            # =================== THUC ===========================
            pyperclip.copy(prompt)
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()

            # ====================================================
#             for row in prompt_split:
#                 query.send_keys(row)
                
#                 ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()

            btnElement = self.driver.find_element(By.XPATH, "//button[@data-testid='send-button']")
            btnElement.click()


        def get_output():
            # Check Done Answering
            kill_time = 0
            max_kill_time = 200

            while kill_time < max_kill_time:
                continue_generating_btn_class = "//button[@class='btn relative btn-neutral whitespace-nowrap border-0 md:border']"
                continue_generating_btn = self.driver.find_elements(By.XPATH, continue_generating_btn_class)
                if len(continue_generating_btn) and continue_generating_btn[0].text == "Continue generating":
                    continue_generating_btn[0].click()
                else:
                    stop_generate_btn = self.driver.find_elements(By.XPATH, "//button[@class='rounded-full border-2 border-gizmo-gray-950 p-1 dark:border-gray-200']")
                    if not len(stop_generate_btn):
                        break

                time.sleep(2)
                kill_time += 2

            outputElements_class_name = "//div[@class='flex flex-grow flex-col max-w-full']" # same with problems
            outputElements = self.driver.find_elements(By.XPATH, outputElements_class_name)
            if not outerHTML_flag:
                output = outputElements[-1].text
            else:
                output = outputElements[-1].get_attribute("outerHTML")
            return output
        # ------------------------------------------------

        if new_chat_flag:
            create_new_chat()
        send_prompt()
        print(self.name, ": Sent.")
        time.sleep(5) # fixed
        over = problems_existed()
        if over is not None:
            output = over
            create_new_chat()
        else:
            output = get_output()
        return output, over
