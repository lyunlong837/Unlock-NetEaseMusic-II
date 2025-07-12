# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0096981BDE5DC469D873F4B6FC9F6F9A09C4D6B86D0A93FC89BB454ECDCE11C8A8007D48D44217DEE75D1641248D21699909294531945111E5B59EA1ED7BA5B08F42C9057D7641E3C38B53112C49C7F429DB5209023C400EC58B36E3BFC657F0161F50FC6060933AB3134BCD7C5534E7C248159F854AD80C79B588BF6FBF7C55BE77F7C22C652C5B482FE949A36FE6BC9D27CAD07C969CDF905290FE4825856A694B076926CD80C15B7107B5B3CD841D05646D0FFF3BD9961A685AEE2529B22EE9A8DA6B0472133A195ABBA0F9CAD40FB037D7A54B7F1B24FAB746B08EDDBE33FE6ADF92384CD5D917E0353642665132406C2BFA27CDBB8F83D56494A7954E977CC8F45146A321B6D3C1448E7AAF3E21906DBE8E61EDB3AE6246E437788AE531669D56F4D9D3B98B6DC4CC91BEB77255DCB1B97137B3B4B7C1899F707799D9AC3389994D447FDEC2BBF275B364041E8B454A74BE057B2F1EACD73E25A398918A69"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
