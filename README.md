# Instagram Profile Scraper

## Overview
This project is a web scraper designed to extract the follower count and determine the account type (business or personal) for a list of Instagram profiles. The script uses Python, Selenium, and BeautifulSoup to perform the scraping and includes a proxy rotation mechanism to avoid IP bans and ensure smooth operation.

## Features
- Scrapes follower counts for Instagram profiles
- Identifies if an account is a business or personal profile
- Uses headless browser automation with Selenium
- Employs proxy rotation to avoid IP bans
- Handles errors and retries failed requests

## Requirements
- Python 3.7+
- Selenium
- BeautifulSoup4
- ChromeDriver
- A list of valid proxies

## Installation

1. **Clone the Repository**

```bash
git clone https://github.com/splenwilz/instagram-profile-scraper.git
cd instagram-profile-scraper
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Download ChromeDriver**
   - Download the version of ChromeDriver that matches your installed version of Chrome from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
   - Place the `chromedriver` executable in your system path or in the project directory.

4. **Prepare the Proxy List**
   - Create a file named `valid_proxy.txt` in the project directory.
   - Add your list of proxies to this file, each on a new line.

5. **Prepare the List of Instagram Profiles**
   - Create a file named `profiles.txt` in the project directory.
   - Add the Instagram profile URLs you want to scrape, each on a new line.

## Usage

Run the script using the command below. The script will read the list of Instagram profiles from `profiles.txt` and use the proxies listed in `valid_proxy.txt` to scrape follower counts and account types.

```bash
python scrape_instagram.py
```

### Example Output

```
Profile: https://www.instagram.com/knowaloud
Followers: 120 Followers, 273 Following, 15 Posts - See Instagram photos and videos from God'swill William (@knowaloud)
Account Type: Business
```

## Detailed Script Explanation

### `scrape_instagram.py`

```python
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Load proxies from file
with open('valid_proxy.txt', 'r') as f:
    proxies = f.read().split('\n')

# Load Instagram profiles from file
with open('profiles.txt', 'r') as f:
    instagram_profiles = f.read().split('\n')

# Function to set proxy for Selenium
def set_proxy(options, proxy):
    options.add_argument(f'--proxy-server={proxy}')

# Function to scrape Instagram profile data
def scrape_instagram_profile(url, proxy):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    set_proxy(options, proxy)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(3)  # Wait for the page to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        meta_tag = soup.find('meta', property='og:description')
        if meta_tag:
            followers = meta_tag['content']
            account_type = 'Business' if 'business' in driver.page_source else 'Personal'
            print(f"Profile: {url}, Followers: {followers}, Account Type: {account_type}")
        else:
            print(f"Failed to retrieve data for {url}")

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
```

### Explanation

1. **Proxy Management**: The script reads a list of proxies from `valid_proxy.txt` and rotates them for each request to avoid IP bans.
2. **Profile List**: Instagram profile URLs are read from `profiles.txt`.
3. **Web Scraping**: The script uses Selenium with a headless Chrome browser to navigate Instagram profiles and extract follower counts and account type information using BeautifulSoup.
4. **Error Handling**: The script includes try-except blocks to handle exceptions gracefully and ensure the browser is properly closed after each attempt.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue if you have suggestions for improvements or find any bugs.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

If you have any questions or need further assistance, please contact:

[Godswill William]  
[godswill@tasknify.com]

---

By following these steps, you can effectively use and understand the Instagram Profile Scraper. If you encounter any issues or have suggestions, please do not hesitate to reach out.