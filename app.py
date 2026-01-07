import sys,os,time,json,argparse,random
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import gzip
from threading import Thread,current_thread
from decouple import config
import firebase


MAX_THREADS = int(config('MAX_THREADS'))
RANGE_SET = int(config('RANGE_SET'))
JWT_VALUE = config('TOKEN')
session = "Global Scope for debugging"

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--remote-debugging-port=9222')


chrome_options.add_argument("--disable-dev-shm-usage")     # avoid /dev/shm mount issues
driver_path = '/usr/local/bin/chromedriver'

# ─── extra “lightweight” flags ────────────────────────────────────────────

# 1. Slash extra processes ↓
# chrome_options.add_argument("--single-process") # Crashes threaded 
chrome_options.add_argument("--no-zygote")
chrome_options.add_argument("--disable-zygote")

# 2. Turn off GPU & rendering tricks ↓
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")

# 3. Skip unneeded services ↓
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-dev-shm-usage")         
chrome_options.add_argument("--disable-background-timer-throttling")
chrome_options.add_argument("--disable-backgrounding-occluded-windows")
chrome_options.add_argument("--disable-breakpad")
chrome_options.add_argument("--disable-client-side-phishing-detection")
chrome_options.add_argument("--disable-default-apps")
chrome_options.add_argument("--disable-sync")
chrome_options.add_argument("--disable-translate")

# 4. Shrink caching & logs ↓
# chrome_options.add_argument("--disk-cache-size=0")
# chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--hide-scrollbars")
chrome_options.add_argument("--log-level=3")

# service = ChromeService(executable_path=driver_path)
service = ChromeService(executable_path=ChromeDriverManager().install())
colors = ["\033[95m","\033[91m","\033[92m","\033[96m","\033[93m"]
totalXP = totalFixes = 0

def getThreadId():
    thread_name = current_thread().name
    thread_id = int(thread_name.split('#')[1])
    return thread_id%5

def getAndAddTotalXp():
    global totalXP
    totalXP+=5
    firebase.writeXp(5)
    return totalXP

def getTotalXP():
    global totalXP
    return totalXP

def getTotalFixes():
    global totalFixes
    totalFixes+=1
    firebase.writeFailed()
    return totalFixes  

def toogleGear(driver):
    # it's close button's selector we can target gear by using siblingElement
    gear = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-test="quit-button"]'))
    )
    driver.execute_script("arguments[0].nextElementSibling.click();",gear)
    switch = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[aria-pressed="true"]'))
    )
    driver.execute_script("arguments[0].click();",switch)
    done_button = driver.find_element(By.CSS_SELECTOR, '#overlays > div:nth-child(6) > div > div > div > button')
    done_button.click()

def solve(driver,challanges):
    for challange in challanges:
        
        type = challange.get('challengeGeneratorIdentifier').get('specificType')
        if type=="tap" or type=="reverse_tap" or type=="listen_tap":
            answers = challange.get('correctTokens')
            options = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, '[data-test="word-bank"] > div > span > button'))
            )
            time.sleep(1)
            for answer in answers:
                for option in options:
                    if option.text==answer:
                        option.click()
                        options.remove(option)
                        time.sleep(.3)
                        break
        elif type == 'assist':
            answers = challange.get('choices')
            options = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, '[data-test="challenge-choice"] > [data-test="challenge-judge-text"]'))
            )
            for option in options:
                if option.text==answers[challange.get('correctIndex')]:
                    option.click()
                    time.sleep(.3)
                    break
        elif type == 'form':
            answers = challange.get('choices')
            options = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'div._35Xo_._9qT-e._3hkYG._2Nv1I > div > div'))
            )
            for option in options:
                if option.text==answers[challange.get('correctIndex')]:
                    option.click()
                    time.sleep(.3)
                    break
        elif type=='reverse_translate' or type == 'translate':
            answer = challange.get('correctSolutions')[0]
            text_area = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-test="challenge-translate-input"]'))
            )
            text_area.send_keys(answer)
            time.sleep(.3)
        elif type=='gap_fill':
            answer = challange.get('choices')[challange.get('correctIndex')]
            options = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'div[role="radiogroup"][aria-label="choice"] > div > [data-test="challenge-judge-text"]'))
            )
            for option in options:
                if option.text==answer:
                    option.click()
                    time.sleep(.3)
                    break
            time.sleep(.3)
        else:
            print(type)
    
        
        next_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[aria-disabled="false"][data-test="player-next"]'))
        )       
        next_btn.click()
        next_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[aria-disabled="false"][data-test="player-next"]'))
        )       
        next_btn.click()
        try:
            time.sleep(1)
            next_btn = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[aria-disabled="false"][data-test="player-next"]'))
            )       
            next_btn.click()
        except:
            pass
    print("{}{} {} +{}xp\033[00m".format(colors[getThreadId()],current_thread().name,'Completed 🔥',getAndAddTotalXp()))  
    try:
        again_btn = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-test="player-practice-again"]'))
            )
        again_btn.click()
        return
    except:
        raise WebDriverException("Mean it' stuck")

def getDriver():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1920,1092)
    return driver

def getPractice(driver):
    try:
        driver.get("https://duolingo.com/")
        driver.add_cookie({'domain':'.duolingo.com','name':'jwt_token','value': JWT_VALUE ,'path':'/'})
        driver.get("https://duolingo.com/practice")
        toogleGear(driver)
        return True
    except Exception as e:
        print("{}Page Not Loaded, Fixing...{}\033[00m".format(colors[getThreadId()],getTotalFixes()))
        try: 
            driver.close()
        except: 
            pass
        del driver
        return False

def core():
    driver = getDriver()
    challanges = None
    if not getPractice(driver): return
    for _ in range(RANGE_SET):
        try:
            for request in driver.requests:
                if request.response and request.url=='https://www.duolingo.com/2023-05-23/sessions':
                    decompressed_data = gzip.decompress(request.response.body)
                    utf_8_data = str(decompressed_data,'utf-8')
                    global session
                    session = json.loads(utf_8_data)
                    challanges = session.get('challenges', [])
                    if 'adaptiveChallenges' in session.keys():
                        adaptive_challenges = session.get('adaptiveChallenges', [])
                        challanges_count = len(challanges)
                        replace_count = min(len(adaptive_challenges), challanges_count)
                        if replace_count > 0:
                            # Replace the last `replace_count` elements in `challenges` with `adaptive_challenges`
                            challanges[-replace_count:] = adaptive_challenges[:replace_count]
                        # try:
                        #     challanges[challanges_count-1] = session.get('adaptiveChallenges')[1]
                        #     challanges[challanges_count-2] = session.get('adaptiveChallenges')[0]
                        # except:
                        #     challanges[challanges_count-1] = session.get('adaptiveChallenges')[0]
                    break
        except ValueError:
            print("\033[91mRESTARTING CONTAINER\033[00m")
            sys.exit(1)
        if not challanges:
            time.sleep(5)
        else:
            del driver.requests
            try:
                solve(driver,challanges)
                challanges = None
            except WebDriverException:
                print("{}Fixing...{}\033[00m".format(colors[getThreadId()],getTotalFixes()))
                try: 
                    driver.close()
                except: 
                    pass
                del driver
                return
    return
    
def startThreadMonitor(threads):
    while True:
        try:
            for i in range(len(threads)):
                thread = threads[i]
                if not thread.is_alive():
                    new_thread = Thread(target=core,name=thread.name)
                    new_thread.start()
                    threads[i] = new_thread
                    del thread
                    time.sleep(2) # To reduce simultaneous opening errors
            time.sleep(10)
        except KeyboardInterrupt:
            return
        except:
            print('Error Occured in Handeler')

            

if __name__ == "__main__":
    namedThreads = [Thread(name=f"Duohacker#{i}") for i in range(MAX_THREADS)]
    firebase.initialize_firebase()
    firebase.disposePrevious()
    startThreadMonitor(namedThreads)
