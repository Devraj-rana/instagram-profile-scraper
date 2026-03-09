# Instagram Profile Scraper

A Python-based tool that scrapes public Instagram profile data using Selenium and Chrome. Supports login via saved cookies for accessing full profile details including bio, website, and address.

---

## Features

- Scrapes multiple Instagram profiles in a single run
- Extracts: followers, following, post count, bio, hashtags, website, address, account type, verified status, and profile picture URL
- Login session saved as cookies (no repeated manual login)
- Automatic fallback to manual login if cookies expire
- Anti-detection browser options (no headless, custom user-agent)
- Optional proxy support

---

## Data Extracted

| Field        | Description                              |
|--------------|------------------------------------------|
| Username     | Instagram handle + full name             |
| Followers    | Formatted (e.g. 297.9M)                  |
| Following    | Number of accounts followed              |
| Posts        | Total posts count                        |
| Verified     | Whether the account is verified          |
| Account Type | Business / Professional / Private / Personal |
| Bio          | Profile biography text                   |
| Hashtags     | Hashtags found in bio                    |
| Website      | External URL from profile                |
| Address      | Business address (if available)          |
| Profile Pic  | URL of the profile picture               |

---

## Requirements

- Python 3.8+
- Google Chrome installed
- Dependencies listed in `requirements.txt`

---

## Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd instagram-profile-scraper
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\Activate.ps1
   # Mac/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your Instagram credentials** in `scrape_instagram.py`:
   ```python
   INSTAGRAM_USERNAME = "your_username"
   INSTAGRAM_PASSWORD = "your_password"
   ```

5. **Add profiles to scrape** in `profiles.txt` (one URL per line):
   ```
   https://www.instagram.com/nike/
   https://www.instagram.com/nasa/
   ```

---

## Usage

```bash
python scrape_instagram.py
```

On first run, a browser window will open for login. After successful login, the session is saved to `instagram_cookies.pkl` and reused on future runs.

---

## Configuration

In `scrape_instagram.py`:

| Variable      | Default | Description                          |
|---------------|---------|--------------------------------------|
| `USE_LOGIN`   | `True`  | Enable login for full data access    |
| `USE_PROXIES` | `False` | Enable proxy rotation                |
| `COOKIE_FILE` | `instagram_cookies.pkl` | Path to saved session file |

---

## File Structure

```
instagram-profile-scraper/
├── scrape_instagram.py       # Main scraper script
├── profiles.txt              # List of Instagram profile URLs to scrape
├── requirements.txt          # Python dependencies
├── instagram_cookies.pkl     # Saved login session (auto-generated)
└── README.md
```

---

## Notes

- Cookies expire periodically (Instagram enforces session limits). Re-login will be prompted automatically.
- Running too many requests too fast may trigger Instagram rate limiting. The script adds random delays between profiles to reduce this risk.
- Scraping violates Instagram's Terms of Service. Use responsibly and only for personal/educational purposes.

---

## .gitignore Recommendations

Add these to `.gitignore` to avoid leaking credentials or sessions:
```
instagram_cookies.pkl
.venv/
__pycache__/
```
