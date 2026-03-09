from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Function to get follower count and account type
def get_instagram_data(username):
    url = f"https://www.instagram.com/{username}/"
    driver.get(url)
    time.sleep(3)  # Wait for the page to load

    try:
        # Get follower count
        followers = driver.find_element(By.XPATH, "//a[contains(@href, '/followers')]/span").get_attribute('title')
        
        # Get account type (business/professional or not)
        account_type_element = driver.find_element(By.XPATH, "//div[contains(@class, 'v9tJq')]//span")
        account_type = 'Professional' if 'Business' in account_type_element.text or 'Creator' in account_type_element.text else 'Personal'
        
        return followers, account_type
    except Exception as e:
        return None, None

# Example usage
username = "example_username"
followers, account_type = get_instagram_data(username)
print(f"Username: {username}, Followers: {followers}, Account Type: {account_type}")

# Close the driver
driver.quit()
