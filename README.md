# Social Media Scraper

## Overview
Social Media Scraper is a Python-based tool designed to extract and collect data from popular social media platforms including **Twitter**, **YouTube**, and **Instagram**. It automates data scraping such as posts, videos, and user interactions, making it ideal for data collection, research, and analysis.

---

## Features
- Scrape YouTube video details like title, views, and posting time.
- Extract tweets, retweets, and user data from Twitter.
- Collect Instagram posts, media details, and interactions.
- Configurable scraping limits and credentials via `config.py`.
- Saves scraped data as CSV files organized by platform.
- Logs scraping processes and errors using the `loguru` logger.
- Runs in headless mode by default using Selenium WebDriver.

---

## Project Structure

```

Social Media Scraper/
├── README.md
├── config.py                 # Configuration for credentials, paths, and scraping parameters
├── logs/                     # Log files generated during scraping
├── main.py                   # Main entry point to select platform and start scraping
├── platforms/                # Platform-specific scraping modules
│   ├── instagram/
│   │   ├── dataset/          # Instagram scraped datasets
│   │   └── main.py           # Instagram scraping logic
│   ├── twitter/
│   │   ├── dataset/          # Twitter scraped datasets
│   │   └── main.py           # Twitter scraping logic
│   └── youtube/
│       ├── dataset/          # YouTube scraped datasets
│       └── main.py           # YouTube scraping logic
└── webdriver/
└── chromedriver          # Selenium ChromeDriver executable

````

---

## Getting Started

### Prerequisites

- Python 3.10
- Google Chrome browser installed
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) matching your Chrome version placed in `webdriver/chromedriver`
- Install required Python packages:

```bash
pip install selenium loguru pandas deep_translator beautifulsoup4
````
---

### Configuration (`config.py`)

Modify the following parameters in `config.py` according to your needs:

```python
# YouTube
YOUTUBE_CHANNEL = "CHANNEL NAME"
YOUTUBE_SCROLL_LIMIT = 2

# Twitter
TWITTER_USERNAME = "YOUR_TWITTER_USERNAME"
TWITTER_PASSWORD = "YOUR_TWITTER_PASSWORD"
TWITTER_HANDLE = "TARGET_TWITTER_HANDLE"
TWITTER_DATE_LIMIT = (datetime.now() - timedelta(days=1))  # Scrape tweets from last 1 day

# Instagram
INSTAGRAM_USERNAME = "YOUR_INSTAGRAM_USERNAME"
INSTAGRAM_PASSWORD = "YOUR_INSTAGRAM_PASSWORD"
INSTAGRAM_HANDLE = "TARGET_INSTAGRAM_HANDLE"
INSTAGRAM_DATE_LIMIT = (datetime.now() - timedelta(days=1))  # Scrape posts from last 1 day

# WebDriver
HEADLESS = True   # Run browser in headless mode (no GUI)
```

This file also manages folder creation for logs and datasets, and sets up Selenium WebDriver with Chrome options.

---

### Running the Scraper

Run the main script:

```bash
python main.py
```

You will be prompted to choose a platform:

```
Enter the number to choose the platform:
[1] Twitter
[2] YouTube
[3] Instagram
```

Enter the number corresponding to your desired platform, and the scraper will begin collecting data based on your config.

Scraped data will be saved in the respective platform's `dataset` folder in CSV format.

Logs are saved under the `logs/` directory.

---

## Notes

* Make sure your credentials in `config.py` are correct and that your accounts allow automated scraping.
* This tool uses Selenium WebDriver and ChromeDriver; ensure compatibility between Chrome and ChromeDriver versions.
* The scraper runs in headless mode by default for efficiency but can be toggled by setting `HEADLESS = False` in `config.py`.
