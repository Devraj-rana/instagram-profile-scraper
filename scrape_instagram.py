from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import random
import time
import pickle
import os
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS = True
except ImportError:
    COLORS = False
    class Fore:
        CYAN=GREEN=YELLOW=RED=MAGENTA=BLUE=WHITE=RESET=''
    class Back:
        RESET=''
    class Style:
        BRIGHT=DIM=RESET_ALL=''

def c(text, color, bright=False):
    if not COLORS:
        return text
    return f"{Style.BRIGHT if bright else ''}{color}{text}{Style.RESET_ALL}"

import unicodedata, re as _re
_ANSI = _re.compile(r'\x1b\[[0-9;]*m')
def vlen(text):
    """Visual terminal width: strips ANSI codes, counts wide chars as 2."""
    plain = _ANSI.sub('', str(text))
    width = 0
    for ch in plain:
        eaw = unicodedata.east_asian_width(ch)
        width += 2 if eaw in ('W', 'F') else 1
    return width

def vljust(text, width):
    """Left-justify text to visual width, padding with spaces."""
    return text + ' ' * max(0, width - vlen(text))

# ============ CONFIGURATION ============
# Instagram Login Credentials (REQUIRED for bio scraping)
INSTAGRAM_USERNAME = "randomaccount2k26_ok1"  # Change this to your Instagram username
INSTAGRAM_PASSWORD = "vanshgupta"  # Change this to your Instagram password

# Set to True to use proxies, False to run without proxies
USE_PROXIES = False

# Set to True to use login (enables bio and more data), False to scrape without login
USE_LOGIN = True

# Cookie file to save login session (avoids logging in every time)
COOKIE_FILE = "instagram_cookies.pkl"
# ========================================

# Load proxies from file (if using proxies)
if USE_PROXIES:
    with open('valid_proxy.txt', 'r') as f:
        proxies = [p.strip() for p in f.read().split('\n') if p.strip()]

# Load Instagram profiles from file
with open('profiles.txt', 'r') as f:
    instagram_profiles = [p.strip() for p in f.read().split('\n') if p.strip()]

print(f"Loaded {len(instagram_profiles)} profile(s) from profiles.txt:")
for i, profile in enumerate(instagram_profiles, 1):
    print(f"  {i}. {profile}")
print()

# Function to initialize driver
def init_driver(proxy=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Comment out headless mode for login (Instagram detects headless browsers)
    # options.add_argument('--headless')
    
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Function to save cookies
def save_cookies(driver, filepath):
    pickle.dump(driver.get_cookies(), open(filepath, "wb"))
    print(f"✓ Cookies saved to {filepath}")

# Function to load cookies
def load_cookies(driver, filepath):
    if os.path.exists(filepath):
        cookies = pickle.load(open(filepath, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        print(f"✓ Cookies loaded from {filepath}")
        return True
    return False

# Dismiss common Instagram popups ("Save Login Info", "Turn on Notifications")
def dismiss_popups(driver):
    not_now_xpaths = [
        "//button[contains(text(), 'Not now') or contains(text(), 'Not Now')]",
        "//div[@role='button' and (contains(text(), 'Not now') or contains(text(), 'Not Now'))]",
    ]
    for _ in range(2):  # Try up to 2 popups
        time.sleep(2)
        for xpath in not_now_xpaths:
            try:
                btn = driver.find_element(By.XPATH, xpath)
                btn.click()
                print("✓ Dismissed popup")
                break
            except:
                continue

# Check if currently logged in
def is_logged_in(driver):
    try:
        driver.find_element(By.XPATH, "//svg[@aria-label='Home']")
        return True
    except:
        return False

# Function to login to Instagram
def instagram_login(driver):
    print("\n" + "="*60)
    print("INSTAGRAM LOGIN")
    print("="*60)

    driver.get("https://www.instagram.com/")
    time.sleep(3)

    # ── 1. Try saved cookies first ──────────────────────────────────────────
    if load_cookies(driver, COOKIE_FILE):
        driver.refresh()
        time.sleep(4)
        if is_logged_in(driver):
            print("✓ Logged in successfully using saved cookies!")
            print("="*60 + "\n")
            return True
        else:
            print("⚠ Saved cookies expired, attempting automatic login...")

    # ── 2. Automatic login using credentials ────────────────────────────────
    print("\n🤖 Attempting automatic login...")
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(4)

        # Fill username
        username_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username'], input[aria-label*='username' i], input[aria-label*='email' i]"))
        )
        username_field.clear()
        username_field.send_keys(INSTAGRAM_USERNAME)
        time.sleep(1)

        # Fill password
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password'], input[type='password']"))
        )
        password_field.clear()
        password_field.send_keys(INSTAGRAM_PASSWORD)
        time.sleep(1)

        # Click Login button
        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_btn.click()
        time.sleep(7)  # Wait for login / 2FA / challenge

        if is_logged_in(driver):
            print("✓ Automatic login successful!")
            dismiss_popups(driver)
            save_cookies(driver, COOKIE_FILE)
            print("✓ Session saved for future runs.")
            print("="*60 + "\n")
            return True
        else:
            # Instagram may show a challenge/2FA page
            print("⚠ Automatic login failed (challenge or 2FA detected).")
            print("  Please complete verification in the browser window.")
            input("\n👉 Press ENTER after you've completed verification and see your feed: ")
            if is_logged_in(driver):
                dismiss_popups(driver)
                save_cookies(driver, COOKIE_FILE)
                print("✓ Login verified and session saved!")
                print("="*60 + "\n")
                return True

    except Exception as e:
        print(f"⚠ Auto-login error: {e}")

    # ── 3. Fallback: full manual login ──────────────────────────────────────
    print("\n📱 MANUAL LOGIN REQUIRED")
    print("-" * 60)
    print("The browser window is open. Please:")
    print("1. Login to Instagram manually in the browser")
    print("2. Complete any verification if required")
    print("3. Wait until you see your Instagram feed")
    print("4. Then press ENTER in this terminal to continue")
    print("-" * 60)
    driver.get("https://www.instagram.com/accounts/login/")
    input("\n👉 Press ENTER after you've logged in and see your feed: ")
    time.sleep(2)

    dismiss_popups(driver)
    try:
        save_cookies(driver, COOKIE_FILE)
        print("✓ Session saved!")
    except:
        pass
    print("="*60 + "\n")
    return True

# Function to scrape Instagram profile data
def scrape_instagram_profile(driver, url):
    import json
    import re

    try:
        username = url.rstrip('/').split('/')[-1]

        # ── Primary: Instagram internal JSON API (requires login cookies) ───
        # Inject required header so the API returns the target user, not the logged-in user
        try:
            driver.execute_cdp_cmd("Network.enable", {})
            driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
                "headers": {"X-IG-App-ID": "936619743392459"}
            })
        except Exception:
            pass

        api_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        driver.get(api_url)
        time.sleep(3)

        user = None
        try:
            # Chrome may render JSON in a <pre> tag or directly as body text
            raw = driver.find_element(By.TAG_NAME, "pre").text
        except Exception:
            raw = driver.find_element(By.TAG_NAME, "body").text
        try:
            data = json.loads(raw)
            user = data.get("data", {}).get("user", {})
        except Exception:
            pass

        if user:
            # ── Numbers ──────────────────────────────────────────────────────
            def fmt(n):
                if not isinstance(n, (int, float)):
                    return str(n)
                if n >= 1_000_000:
                    return f"{n/1_000_000:.1f}M"
                if n >= 1_000:
                    return f"{n/1_000:.1f}K"
                return f"{n:,}"

            followers = fmt(user.get("edge_followed_by", {}).get("count", "N/A"))
            following = fmt(user.get("edge_follow",      {}).get("count", "N/A"))
            posts     = fmt(user.get("edge_owner_to_timeline_media", {}).get("count", "N/A"))

            # ── Bio & hashtags ───────────────────────────────────────────────
            bio_raw = user.get("biography") or user.get("bio") or ""
            bio = bio_raw.strip() or "No bio set"
            hashtags = re.findall(r'#\w+', bio)

            # ── Website / external URL ────────────────────────────────────────
            website = (
                user.get("external_url")
                or user.get("bio_links", [{}])[0].get("url", "")
                if user.get("bio_links") else user.get("external_url", "")
            ) or "N/A"

            # ── Address (business accounts) ───────────────────────────────────
            address = "N/A"
            addr_json = user.get("business_address_json")
            if addr_json:
                try:
                    addr = json.loads(addr_json) if isinstance(addr_json, str) else addr_json
                    parts = [
                        addr.get("street_address", ""),
                        addr.get("city_name", ""),
                        addr.get("region_name", ""),
                        str(addr.get("zip_code", "") or ""),
                    ]
                    address = ", ".join(p for p in parts if p).strip(", ") or "N/A"
                except Exception:
                    pass
            if address == "N/A":
                # flat fields fallback
                city = user.get("city_name", "") or user.get("city_id", "")
                address = str(city) if city else "N/A"

            # ── Verified ─────────────────────────────────────────────────────
            is_verified = bool(user.get("is_verified") or user.get("verified"))

            # ── Account type ─────────────────────────────────────────────────
            if user.get("is_business_account"):
                account_type = "Business"
            elif user.get("is_professional_account"):
                account_type = "Professional"
            elif user.get("is_private"):
                account_type = "Private"
            else:
                account_type = "Personal (Public)"

            # ── Profile picture ──────────────────────────────────────────────
            pfp = user.get("profile_pic_url_hd") or user.get("profile_pic_url", "N/A")

            # ── Full name ────────────────────────────────────────────────────
            full_name = user.get("full_name", username)

        else:
            # ── Fallback: parse HTML page source (no login / API blocked) ───
            driver.get(url)
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, 400);")
            time.sleep(2)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            def extract(patterns, default="N/A"):
                for pat in patterns:
                    m = re.search(pat, page_source)
                    if m:
                        val = m.group(1).strip()
                        if val:
                            return val
                return default

            followers = following = posts = "N/A"
            meta_desc = soup.find("meta", property="og:description")
            if meta_desc and meta_desc.get("content"):
                desc = meta_desc["content"]
                m_fol  = re.search(r'([\d,\.]+[KkMm]?)\s*Followers', desc, re.IGNORECASE)
                m_fing = re.search(r'([\d,\.]+[KkMm]?)\s*Following', desc, re.IGNORECASE)
                m_post = re.search(r'([\d,\.]+[KkMm]?)\s*Posts?',    desc, re.IGNORECASE)
                if m_fol:  followers = m_fol.group(1)
                if m_fing: following = m_fing.group(1)
                if m_post: posts     = m_post.group(1)

            pfp = "N/A"
            meta_img = soup.find("meta", property="og:image")
            if meta_img and meta_img.get("content"):
                pfp = meta_img["content"]

            bio = extract([
                r'"biography"\s*:\s*"((?:[^"\\]|\\.)*)"',
                r'biography&quot;:&quot;(.*?)(?:&quot;|\\u0022)',
            ], default="No bio set")
            try:
                bio = bio.encode("latin1").decode("unicode_escape")
            except Exception:
                bio = bio.replace("\\n", " ").replace("\\u0026", "&")
            bio = bio.strip()

            hashtags    = re.findall(r'#\w+', bio)
            is_verified = bool(re.search(r'"is_verified"\s*:\s*true|"verified"\s*:\s*true', page_source))
            full_name   = extract([r'"full_name"\s*:\s*"((?:[^"\\]|\\.)*)"'], default=username)
            website     = extract([r'"external_url"\s*:\s*"((?:[^"\\]|\\.)*)"'], default="N/A")
            address     = extract([r'"business_address_json"\s*:\s*"((?:[^"\\]|\\.)*)"'], default="N/A")

            if re.search(r'"is_business_account"\s*:\s*true', page_source):
                account_type = "Business"
            elif re.search(r'"is_professional_account"\s*:\s*true', page_source):
                account_type = "Professional"
            elif re.search(r'"is_private"\s*:\s*true', page_source):
                account_type = "Private"
            else:
                account_type = "Personal (Public)"

        # ── Print result ──────────────────────────────────────────────────────
        W = 62
        verified_str = c("✔ Verified", Fore.GREEN, bright=True) if is_verified else c("✘ Not Verified", Fore.RED)
        type_colors = {
            "Business": Fore.YELLOW,
            "Professional": Fore.CYAN,
            "Private": Fore.RED,
            "Personal (Public)": Fore.GREEN,
        }
        type_str = c(account_type, type_colors.get(account_type, Fore.WHITE), bright=True)

        print()
        print(c("╔" + "═" * (W-2) + "╗", Fore.CYAN))
        # Header
        header = f"  @{username}"
        if full_name and full_name != username:
            header += f"  ·  {full_name}"
        print(c("║", Fore.CYAN) + c(vljust(header, W-2), Fore.WHITE, bright=True) + c("║", Fore.CYAN))
        print(c("╠" + "═" * (W-2) + "╣", Fore.CYAN))

        # Stats row
        def stat_block(label, value, color):
            val = c(str(value), color, bright=True)
            lbl = c(label, Fore.WHITE)
            return f"  {lbl}: {val}"

        stats_line = (
            stat_block("Followers", followers, Fore.MAGENTA) + "   "
            + stat_block("Following", following, Fore.BLUE) + "   "
            + stat_block("Posts", posts, Fore.YELLOW)
        )
        # Print plain version for padding, colored version for display
        plain_stats = f"  Followers: {followers}   Following: {following}   Posts: {posts}"
        pad = W - 2 - vlen(plain_stats)
        print(c("║", Fore.CYAN) + stats_line + " " * max(pad, 0) + c("║", Fore.CYAN))
        print(c("╠" + "═" * (W-2) + "╣", Fore.CYAN))

        # Details
        def row(icon, label, value, val_color=Fore.WHITE):
            label_part = c(f" {icon} {label:<13}", Fore.CYAN)
            value_part = c(str(value), val_color)
            plain = f" {icon} {label:<13}{value}"
            pad = W - 2 - vlen(plain)
            print(c("║", Fore.CYAN) + label_part + value_part + " " * max(pad, 0) + c("║", Fore.CYAN))

        row("◈", "Status",       verified_str if is_verified else c("✘ Not Verified", Fore.RED), "")
        row("◈", "Account",      type_str, "")
        row("◈", "Bio",          bio[:45] + ("..." if len(bio) > 45 else ""), Fore.WHITE)
        if hashtags:
            row("◈", "Hashtags",  " ".join(hashtags)[:45], Fore.YELLOW)
        if website != "N/A":
            row("◈", "Website",   website[:45] + ("..." if len(website) > 45 else ""), Fore.CYAN)
        if address != "N/A":
            row("◈", "Address",   address[:45] + ("..." if len(address) > 45 else ""), Fore.WHITE)

        print(c("╚" + "═" * (W-2) + "╝", Fore.CYAN))
        print()

    except Exception as e:
        print(c(f"  ✗  Error scraping {url}: {e}", Fore.RED) + "\n")

# ============ MAIN EXECUTION ============
if __name__ == "__main__":
    driver = None
    try:
        W = 62
        print()
        print(c("╔" + "═" * (W-2) + "╗", Fore.CYAN))
        title = "INSTAGRAM PROFILE SCRAPER"
        print(c("║", Fore.CYAN) + c(title.center(W-2), Fore.WHITE, bright=True) + c("║", Fore.CYAN))
        print(c("╚" + "═" * (W-2) + "╝", Fore.CYAN))
        print()

        # Check if saved login exists
        if os.path.exists(COOKIE_FILE):
            print(c(f"  ✔  Found saved login session: {COOKIE_FILE}", Fore.GREEN))
        else:
            print(c(f"  ℹ  No saved session found — will need to login", Fore.YELLOW))
        print()
        
        # Initialize driver
        proxy = random.choice(proxies) if USE_PROXIES else None
        driver = init_driver(proxy)
        
        # Login to Instagram if enabled
        if USE_LOGIN:
            if INSTAGRAM_USERNAME == "your_username" or INSTAGRAM_PASSWORD == "your_password":
                print(c("  ⚠  Please update INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in the script!", Fore.YELLOW))
                print(c("  Continuing without login (bio will not be available)...\n", Fore.YELLOW))
                USE_LOGIN = False
            else:
                if not instagram_login(driver):
                    print(c("  ⚠  Login failed. Continuing without login (bio will not be available)...\n", Fore.YELLOW))
        else:
            print(c("  ℹ  Login disabled (USE_LOGIN = False). Bio data will not be available.\n", Fore.YELLOW))

        total = len(instagram_profiles)
        # Scrape all profiles using the same driver session
        for i, profile in enumerate(instagram_profiles, 1):
            print(c(f"  ──  [{i}/{total}] Scraping: ", Fore.CYAN) + c(profile, Fore.WHITE, bright=True))
            scrape_instagram_profile(driver, profile)

            # Random delay between profiles (except for the last one)
            if i < total:
                delay = random.uniform(3, 6)
                time.sleep(delay)

        print(c(f"  ✔  Finished scraping all {total} profile(s).", Fore.GREEN))
        
    except Exception as e:
        print(c(f"  ✗  Error in main execution: {e}", Fore.RED))

    finally:
        if driver:
            driver.quit()
            print(c("  ✔  Browser closed.", Fore.GREEN))
