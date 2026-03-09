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

# # List of Instagram profiles to scrape
instagram_profiles = [
    'https://www.instagram.com/knowaloud'
]

# Load Instagram profiles from file
# with open('profiles.txt', 'r') as f:
#     instagram_profiles = f.read().split('\n')

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


# import random
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup

# # Load proxies from file
# with open('valid_proxy.txt', 'r') as f:
#     proxies = f.read().split('\n')

# # Load Instagram profiles from file
# with open('profiles.txt', 'r') as f:
#     instagram_profiles = f.read().split('\n')

# # Function to set proxy for Selenium
# def set_proxy(options, proxy):
#     options.add_argument(f'--proxy-server={proxy}')

# # Function to scrape Instagram profile data
# def scrape_instagram_profile(url, proxy):
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     set_proxy(options, proxy)
    
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#     try:
#         driver.get(url)
#         time.sleep(3)  # Wait for the page to load

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         meta_tag = soup.find('meta', property='og:description')
#         if meta_tag:
#             followers = meta_tag['content']
#             account_type = 'Business' if 'business' in driver.page_source else 'Personal'
#             print(f"Profile: {url}, Followers: {followers}, Account Type: {account_type}")
#         else:
#             print(f"Failed to retrieve data for {url}")

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         driver.quit()

# # Main loop to iterate through Instagram profiles and proxies
# for profile in instagram_profiles:
#     proxy = random.choice(proxies)
#     scrape_instagram_profile(profile, proxy)
#     time.sleep(random.uniform(1, 5))  # Random delay between requests

# print("Finished scraping profiles.")


# import time
# import random
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup

# def scrape_instagram_profile(profile_url, proxy):
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--proxy-server=%s' % proxy)
    
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver.get(profile_url)
    
#     time.sleep(random.uniform(3, 6))  # Wait for the page to load
    
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     driver.quit()
    
#     # Extract the relevant data
#     followers = soup.find('span', {'class': 'g47SY'}).get('title')
#     following = soup.find_all('span', {'class': 'g47SY'})[1].text
#     posts = soup.find_all('span', {'class': 'g47SY'})[0].text
#     account_type = 'Business' if 'business' in soup.text.lower() else 'Personal'

#     return {
#         'profile': profile_url,
#         'followers': followers,
#         'following': following,
#         'posts': posts,
#         'account_type': account_type
#     }

# if __name__ == '__main__':
#     proxies = ['proxy1', 'proxy2', 'proxy3']  # Add your list of proxies
#     profiles = [
#         'https://www.instagram.com/knowaloud',
#         'https://www.instagram.com/davido',
#         # Add more profiles here
#     ]
    
#     results = []
    
#     for i, profile in enumerate(profiles):
#         try:
#             proxy = proxies[i % len(proxies)]
#             result = scrape_instagram_profile(profile, proxy)
#             results.append(result)
#             print(result)
#         except Exception as e:
#             print(f"Error scraping {profile}: {e}")
        
#         time.sleep(random.uniform(10, 20))  # Random delay between requests

#     print("Finished scraping profiles.")
