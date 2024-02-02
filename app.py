import os, sys
this_path = os.path.abspath(os.path.dirname(__file__))
if this_path not in sys.path:
    sys.path.append(this_path)
import numpy as np
from flask import Flask, request

app = Flask(__name__)

from threading import Thread
import json
import time
import shutil

# from myDriver import MyDriver
from undetectedChromeDriver import *

machine_name = "1"
api_port = 8081
accounts_json = "accounts.json"
if len(sys.argv) > 1:
    machine_name = sys.argv[1]
if machine_name == "1":
    api_port = 8081
    accounts_json = "accounts.json"
    
with open(accounts_json) as acc_json:
    acc_list = json.load(acc_json)["accounts"]
    acc_json.close()

_headless_ = True
if len(sys.argv) > 2:
    _headless_ = True if sys.argv[2] == "1" else False

freeDrivers = [] # first good last bad
usageCapDriver = 0

def update_accounts_json():
    res = dict()
    res["accounts"] = acc_list
    accounts_path = os.path.join(this_path, accounts_json)
    with open(accounts_path, "w") as outfile:
        json.dump(res, outfile)
    print(f"{accounts_json} has been updated...")

def create_new_browser(acc_i, name, email, passw, idx, cookies, PROXY_FOLDER):
    _time_ = 1
    max_num_try_ = 3
    while _time_ <= max_num_try_:
        print(f"""{name} thu browser lan thu {_time_}""")
        myDriver = MyDriver(name=name, PROXY_FOLDER=PROXY_FOLDER, idx=idx, headless=_headless_)
        res_cookies = myDriver.openai_login(name, email, passw, cookies, time_=1)
        if res_cookies and res_cookies != "Needless":
            acc_list[acc_i]["cookies"] = res_cookies
        
        if ".json" in res_cookies:
            _time_ = 99
        else:
            myDriver.turn_off()
            time.sleep(1.1)
            _time_ += 1
            
    if _time_ == max_num_try_ + 1:
        print(f"""{name} da thu {max_num_try_} lan khoi dong browser""")
        return
    
    try:
        myDriver.skip_popups()
    except: 
        print(f"{myDriver.name} no pop up !")

    print(name, "Logging success!!!")
    # Khang's dummy
    tmp, over = myDriver.chat(prompt="2+3=?", new_chat_flag=True, outerHTML_flag=False)
    print(f"{myDriver.name} tra loi {tmp}", over)
    # myDriver.turn_off()
    # return
    global usageCapDriver
    global freeDrivers
    if over is None:
        freeDrivers.insert(0, myDriver)
    else:
        freeDrivers.append(myDriver)
        usageCapDriver += 1

def start():
    # shutil.rmtree(extension_FOLDER)
    print('START')

    global freeDrivers
    freeDrivers = [] # first good last bad
    global usageCapDriver
    usageCapDriver = 0
    print(len(freeDrivers), usageCapDriver)
    try:
        thr_list = []
        n = len(GetProxyIP.lstApiKey)
        print('lstApiKey', n)
        list_batch_acc = np.array_split(np.array(acc_list[:]),n) # CHUNK to N, Thuc
        for batch_idx, batch in enumerate(list_batch_acc):
            proxy_extension_folder = create_proxy_extension_folder(batch_idx)
    #             proxy_count = 0
    #             while (proxy_count <5):
    #                 proxy_count+=1
    #                 proxy_extension_folder = create_proxy_extension_folder()
    #                 sample_acc = batch[0]
    #                 name, email, passw, cookies = sample_acc["name"], sample_acc["email"], sample_acc["passw"], sample_acc["cookies"]
    #                 my_thread = Thread(target=create_new_browser, args=(0, name, email, passw, cookies, proxy_extension_folder))
    #                 my_thread.start()
    #                 result = my_thread.join()
    #                 print("***"*20)
    #                 print(result)
    #                 print("***"*20)
            for acc_i, acc in enumerate(batch):
                name, email, passw, idx, cookies = acc["name"], acc["email"], acc["passw"], acc["idx"], acc["cookies"]
                thr_list.append(Thread(target=create_new_browser, args=(acc_i, name, email, passw, idx, cookies, proxy_extension_folder)))

        for thr in thr_list:
            thr.start()
            time.sleep(7)

        for thr in thr_list:
            thr.join()
            time.sleep(7)
    except Exception as e:
        print(e)
            
    update_accounts_json()
    print(len(freeDrivers), "browsers are currently available.")
    print(usageCapDriver, "usage cap.")   


@app.route('/', methods=['POST'])
def home():
    output = {
        "output": "Just do it."
    }
    return output, 200


@app.route('/kill', methods=['POST'])
def kill():
    for driver in freeDrivers:
        driver.turn_off()
    output = {
        "output": "Goodbye."
    }
    return output, 200


@app.route('/send_prompt', methods=['POST'])
def send_prompt():

    global freeDrivers
    global usageCapDriver
    def get_available_driver():
        if len(freeDrivers) == 0:
            return None
        freeDriver = freeDrivers[0]
        freeDrivers.pop(0)
        return freeDriver
    
    def try_it(freeDriver, prompt, new_chat_flag, outerHTML_flag):
        print(freeDriver.name, "--> running")
        try:
            gpt_response, over = freeDriver.chat(prompt, new_chat_flag, outerHTML_flag)
        except Exception as e:
            print(freeDriver.name, ": Error occuring while request")
            gpt_response, over = str(e), "error"
        return gpt_response, over
    
    # Check we don't have other windows open already
#     assert len(freeDriver.window_handles) > 5 
    
    form_data = request.form
    prompt = form_data['prompt']
    try:
        new_chat_int = form_data['new_chat']
    except:
        new_chat_int = '1'
    try:
        outerHTML_int = form_data['outerHTML']
    except:
        outerHTML_int = '0'
    new_chat_flag = False if new_chat_int == '0' else True
    outerHTML_flag = False if outerHTML_int == '0' else True

    freeDriver = get_available_driver()
    if not freeDriver:
        return {"output": "All browsers are currently busy"}, None


    gpt_response, over = try_it(freeDriver=freeDriver, prompt=prompt, new_chat_flag=new_chat_flag, outerHTML_flag=outerHTML_flag)
    resp = {"output": gpt_response}

    status_code = 200
    if over is None:
        freeDrivers.insert(0, freeDriver)
    else:
        freeDrivers.append(freeDriver)
        status_code = 500
        usageCapDriver+=1
    print(freeDriver.name, "--> free")
    return resp, status_code


if __name__ == '__main__':
    start()
    app.run(host="0.0.0.0", port=api_port)
