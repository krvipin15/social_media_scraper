# --------------------------------------------------- Required imports ----------------------------------------------

import os
import sys
from loguru import logger
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ------------------------------------------- Change the variables as per requirements --------------------------------

# YouTube Configuration
YOUTUBE_CHANNEL = "CHANNEL NAME"
YOUTUBE_SCROLL_LIMIT = 2

# Twitter Configuration
TWITTER_USERNAME = "USERNAME"
TWITTER_PASSWORD = "PASSWORD"
TWITTER_HANDLE = 'HANDLE NAME'
TWITTER_DATE_LIMIT = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
TWITTER_DATE_LIMIT = datetime.strptime(TWITTER_DATE_LIMIT, "%Y-%m-%d %H:%M:%S")

# Instagram Configration
INSTAGRAM_USERNAME = "USERNAME"
INSTAGRAM_PASSWORD = "PASSWORD"
INSTAGRAM_HANDLE = 'HANDLE NAME'
INSTAGRAM_DATE_LIMIT = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
INSTAGRAM_DATE_LIMIT = datetime.strptime(INSTAGRAM_DATE_LIMIT, "%Y-%m-%d %H:%M:%S")

# Webdriver Configuration
HEADLESS = True

# ------------------------------------------------- No need to change anything ------------------------------------------

# Folder Configration
project_folder = os.getcwd()

# Log Folder
log_folder = os.path.join(project_folder, "logs")
os.makedirs(log_folder, exist_ok=True)
log_file_path = os.path.join(log_folder, f"logs_{datetime.now().strftime('%d-%m-%y_%H:%M:%S')}.log")

# YouTube Folder
yt_folder_path = os.path.join(project_folder, f"platforms/youtube/dataset")
os.makedirs(yt_folder_path, exist_ok=True)
yt_file_path = os.path.join(yt_folder_path, f"{YOUTUBE_CHANNEL}_yt{datetime.now().strftime('%d-%m-%y_%H:%M:%S')}.csv")

# Twitter Folder
tw_folder_path = os.path.join(project_folder, f"platforms/twitter/dataset")
os.makedirs(tw_folder_path, exist_ok=True)
tw_file_path = os.path.join(tw_folder_path, f"{TWITTER_HANDLE}_tw{datetime.now().strftime('%d-%m-%y_%H:%M:%S')}.csv")

# Instagram Folder
ig_folder_path = os.path.join(project_folder, f"platforms/instagram/dataset")
os.makedirs(ig_folder_path, exist_ok=True)
ig_file_path = os.path.join(ig_folder_path, f"{INSTAGRAM_HANDLE}_ig{datetime.now().strftime('%d-%m-%y_%H:%M:%S')}.csv")

# Logging Configration
logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</> | <level>{level}</> | <cyan>{message}</>", level="DEBUG")
logger.add(log_file_path, format="<green>{time:YYYY-MM-DD HH:mm:ss}</> | <level>{level}</> | <cyan>{message}</>", level="DEBUG")

# WebDriver Configration
webdriver_path = os.path.join(project_folder, "webdriver/chromedriver")
service = Service(executable_path=webdriver_path)
options = Options()
options.add_argument("--headless") if HEADLESS else options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-popup-blocking")
driver = webdriver.Chrome(service=service, options=options)
