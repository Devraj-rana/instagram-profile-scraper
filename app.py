from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import random
import time

# Load proxies from file
with open('valid_proxy.txt', 'r') as f:
    proxies = f.read().split('\n')

# List of Instagram profiles to scrape
instagram_profiles = [
    'https://www.instagram.com/knowaloud'
    # Add more profiles here
]

# Function to set proxy for Selenium
def set_proxy(driver, proxy):
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": proxy,
        "ftpProxy": proxy,
        "sslProxy": proxy,
        "proxyType": "MANUAL",
    }
    webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

# Function to scrape Instagram profile data
def scrape_instagram_profile(url, proxy):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    set_proxy(driver, proxy)

    try:
        driver.get(url)
        time.sleep(3)  # Wait for the page to load
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        followers = soup.find('meta', property='og:description')['content']
        account_type = 'Business' if 'business' in driver.page_source else 'Personal'
        print(f"Profile: {url}, Followers: {followers}, Account Type: {account_type}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

# Main loop to iterate through Instagram profiles and proxies
for profile in instagram_profiles:
    proxy = random.choice(proxies)
    scrape_instagram_profile(profile, proxy)
    time.sleep(random.uniform(1, 5))  # Random delay between requests

print("Finished scraping profiles.")
