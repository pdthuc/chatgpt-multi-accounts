import os

from pathlib import Path
import time
import json
import pyperclip

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

from TinProxyService import GetProxyIP

import undetected_chromedriver as uc

from selenium_stealth import stealth

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

import time
from datetime import date
today = date.today()

cur_path = os.getcwd()
extension_FOLDER = os.path.join(os.getcwd(), "extension")

# dd_mm_YY
dmy = today.strftime("%d_%m_%Y")

basic_url = 'https://chat.openai.com/?model=gpt-4'
login_url = 'https://chat.openai.com/auth/login/'
def create_proxy_extension_folder(n):
    # Proxy
    result = GetProxyIP.GetProxyIps(apikey_index=n)
    PROXY_HOST, PROXY_PORT = result["proxyIp"].split(":")[0], result["proxyIp"].split(":")[1]
    PROXY_USER = result["username"]
    PROXY_PASS = result["password"]
    PROXY_FOLDER = os.path.join(extension_FOLDER, f"{PROXY_HOST}_{PROXY_PORT}")
    os.makedirs(PROXY_FOLDER, exist_ok=True)

    manifest_json = """
{
"version": "1.0.0",
"manifest_version": 2,
"name": "Chrome Proxy",
"permissions": [
    "proxy",
    "tabs",
    "unlimitedStorage",
    "storage",
    "<all_urls>",
    "webRequest",
    "webRequestBlocking"
],
"background": {
    "scripts": ["background.js"]
},
"minimum_chrome_version":"22.0.0"
}
"""

    background_js = """
var config = {
    mode: "fixed_servers",
    rules: {
    singleProxy: {
        scheme: "http",
        host: "%s",
        port: parseInt(%s)
    },
    bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
return {
    authCredentials: {
        username: "%s",
        password: "%s"
    }
};
}

chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    with open(f"{PROXY_FOLDER}/manifest.json", "w") as f:
        f.write(manifest_json)
        f.close()
    with open(f"{PROXY_FOLDER}/background.js", "w") as f:
        f.write(background_js)
        f.close()

    return PROXY_FOLDER
    
    
class MyDriver:

    def __init__(self, name="unknown", PROXY_FOLDER = '', idx=0, headless=False):
        self.name = name
        self.idx = idx
        self.caps = DesiredCapabilities.CHROME
        self.caps ['goog:loggingPrefs'] = {'performance': 'ALL'}

        self.options = uc.ChromeOptions()

        # options.add_argument(f'user-agent={userAgent}')
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--window-size=1280,720")
        # options.add_argument("--disable-proxy-certificate-handler")
        # options.add_argument("--disable-content-security-policy")
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument("--private")
        # options.add_argument("--auto-open-devtools-for-tabs")
        if PROXY_FOLDER == '':
            PROXY_FOLDER = create_proxy_extension_folder()
        self.options.add_argument(f"--load-extension={PROXY_FOLDER}")
        # self.driver = uc.Chrome(options=options)
        self.driver = uc.Chrome(options=self.options, desired_capabilities=self.caps, version_main=120 )

        # stealth(
        #     self.driver,
        #     languages = ["en-US", "en"],
        #     vendor = "Google Inc.",
        #     platform = "Win32",
        #     webgl_vendor = "Intel Inc.",
        #     renderer = "Intel Iris OpenGL Engine",
        #     fix_hairline = True,
        # )

        # Open a new window 
        self.driver.execute_script(f"window.open('', '{basic_url}');")
        time.sleep(4)
        # Switch to the new window and open new URL 
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(1)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        print("...............................................")
        
    
    def go_to(self, url_=basic_url, wait_time_=4):
        self.driver.get(url_)
        time.sleep(wait_time_)
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable((By.TAG_NAME, "body")))
        except:
            pass


    def turn_off(self):
        self.driver.quit()


    def save_cookie(self, MAIL):
        cookies_filename = f"""{MAIL}.json"""
        cookies_path = os.path.join(cur_path, "Cookies", cookies_filename)
        Path(cookies_path).write_text(
            json.dumps(self.driver.get_cookies(), indent=4)
        )
        print("Save cookies successfully for", self.name)
        return cookies_filename
    

    def load_cookie(self, cookies_filename):
        load = False
        cookies_path = os.path.join(cur_path, "Cookies", cookies_filename)
        cookies = json.loads(Path(cookies_path).read_text())
        for cookie in cookies:
            try:
                self.driver.add_cookie(cookie)
                load = True
            except:
                continue
        print("Load cookies successfully for", self.name)
        return load
    

    def openai_login(self, NAME, MAIL, PASSWORD, COOKIES, time_):
        res_cookies = ""

        if time_ == 2:
            print(f"""{self.name} dang nhap 2 lan khong thanh cong, khoi dong lai browser""")
            return res_cookies

        print(f"""{self.name} dang nhap lan thu {time_}""")
        
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
            loggin_count = 0 
            loggin_break = False
            while True:
                try:
                    loggin_count += 1

                    try:
                        self.go_to(url_=login_url, wait_time_=3)
                        login_btn_tag = self.driver.find_element(By.XPATH, "//button[@data-testid='login-button']")
                        login_btn_tag.click()
                        time.sleep(4)
                        mail = self.driver.find_element(By.XPATH, "//input[@name='username']")

                        mail.send_keys(MAIL)
                        time.sleep(2)
                        btn = self.driver.find_element(By.XPATH, "//button[@name='action']")
                        btn.click()
                        time.sleep(2)
                        password = self.driver.find_element(By.XPATH, "//input[@name='password']")

                        password.send_keys(PASSWORD)
                    except:
                        break
            
                    if loggin_count == 2:
                        while True:
                            time.sleep(3)
                            try:
                                btnElement = self.driver.find_element(By.XPATH, "//button[@data-testid='send-button']")
                                loggin_break = True
                                break
                            except:
                                pass
                             
                    if loggin_count == 3:
                        break
                        
                    if loggin_break:
                        break
                        
                    time.sleep(2)
    #                 btn = self.driver.find_elements(By.XPATH, "//button[@name='action']")[-1]
                    btn = self.driver.find_elements(By.XPATH, "/html/body/div[1]/main/section/div/div/div/form/div[3]/button")[-1] # THUC test
                    btn.click()
                    time.sleep(2)
                
                   
                except Exception as e:
                    print(e)
                    pass
                
                try:
                    btnElement = self.driver.find_element(By.XPATH, "//button[@data-testid='send-button']")
                    break
                except:
                    pass

            try:
                if "login" in self.driver.current_url:
                    print(self.name, "thu dang nhap lai")
                    return self.openai_login(NAME, MAIL, PASSWORD, COOKIES, time_+1)
            except Exception as e:
                print(self.name, "Loi khi dang nhap lai", e)
            
            res_cookies = self.save_cookie(MAIL=MAIL)
        return res_cookies
    

    def skip_popups(self):
        
        try:
            _try_time_ = 0
            while _try_time_ < 3:
                time.sleep(5)
                div_btn_tag = self.driver.find_element(By.XPATH, "//div[@class='flex w-full flex-col gap-2']")
                tmp_btn = div_btn_tag.find_elements(By.XPATH, ".//button")
                if len(tmp_btn):
                    tmp_btn[self.idx].click()
                    break
                else:
                    _try_time_ += 1
        except:
            pass
        
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
                        "The conversation is too long, please start a new one",
                        "The message you submitted was too long",
                        "account has been deactivated",
                        "You've reached"
                    ]
                    for problem in problems:
                        if problem in lastText:
                            over = lastText
                            break
            return over

        def create_new_chat():
            # self.go_to(url_="https://chat.openai.com/?model=gpt-4", wait_time_=4)
            self.go_to(url_=basic_url, wait_time_=4)


#         def send_prompt():
#             wait = WebDriverWait(self.driver, 120)
#             prompt_split = prompt.split('\n')
#             query = wait.until(
#                     EC.presence_of_element_located((By.XPATH, "//textarea[@id='prompt-textarea']"))
#             )
            
# #             for row in prompt_split:
# #                 query.send_keys(row)
# #                 ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
            
#             # =================== THUC ===========================
#             pyperclip.copy(prompt)
#             query.click()
# #             query.send_keys(Keys.CONTROL + 'v')
#             ActionChains(self.driver).click(query).key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
#             # ====================================================

#             btnElement = self.driver.find_element(By.XPATH, "//button[@data-testid='send-button']")
#             btnElement.click()
        def send_prompt():
            JS_ADD_TEXT_TO_INPUT = """
                var elm = arguments[0], txt = arguments[1];
                elm.value += txt;
                elm.dispatchEvent(new Event('change'));
            """
            wait = WebDriverWait(self.driver, 120)
            prompt_split = prompt.split('\n')
            query = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//textarea[@id='prompt-textarea']"))
            )

            for row in prompt_split:
                self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, query, row)

    #                 query.send_keys(row)
            ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()

            btnElement = self.driver.find_element(By.XPATH, "//button[@data-testid='send-button']")
            btnElement.click()


        def get_output():
            # Check Done Answering
            kill_time = 0
            max_kill_time = 200

            while kill_time < max_kill_time:
                continue_generating_btn_class = "//button[@class='btn relative btn-neutral whitespace-nowrap border-0 md:border']"
                continue_generating_btn = self.driver.find_elements(By.XPATH, continue_generating_btn_class)
                stop_generating_btn_class = "//button[@class='rounded-full border-2 border-gray-950 p-1 dark:border-gray-200']"
                stop_generating_btn = self.driver.find_elements(By.XPATH, stop_generating_btn_class)
                
                if len(continue_generating_btn) and continue_generating_btn[0].text == "Continue generating":
                    continue_generating_btn[0].click()
                elif not len(stop_generating_btn):
                    break

                time.sleep(5)
                kill_time += 5

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
        time.sleep(7) # fixed
        over = problems_existed()
        if over is not None:
            output = over
            create_new_chat()
        else:
            output = get_output()
        return output, over
