# -------------------------------------------------- Imports -------------------------------------------------------------

from config import *
from platforms.youtube.main import extract_yt_content
from platforms.twitter.main import extract_tw_content
from platforms.instagram.main import extract_ig_content

# ---------------------------------------------- Info about the tool -----------------------------------------------------

print("""[-] Social Media Scraper [-]

[+] Description:
    This scraper tool allows users to extract and collect data from various social media platforms. It can scrape
    videos, posts, and other content from supported platforms such as Twitter, YouTube, and Instagram.

    The scraper is designed to be highly configurable, with options to choose a platform, manage scraping limits
    and storing data in the database. This tool is ideal for data collection, analysis, and research.

[+] Features:
    - Extracts YouTube videos data like title, views, and time posted.
    - Scrapes tweets, retweets, and user data from Twitter.
    - Scrapes Instagram posts, interactions, and media details.

[+] Supported Platforms:
    [1] Twitter
    [2] YouTube
    [3] Instagram
""")

# ---------------------------------------------- Working of the tool -----------------------------------------------

# Loop until a valid choice is made
while True:
    # Get user input for the platform choice
    user_choice = input("Enter the number to choose the platform: ")

    # Handle the user's choice
    if user_choice == '1':
        logger.info(f"Scraping data from the Twitter handle: {TWITTER_HANDLE}")
        data = extract_tw_content(TWITTER_USERNAME, TWITTER_PASSWORD, TWITTER_HANDLE, TWITTER_DATE_LIMIT)
        if not data.empty:
            data.to_csv(tw_file_path, sep='|', index=False)
            csv_file_path = tw_file_path
            logger.success(f"Cleaned data saved to {tw_file_path}")
        break

    elif user_choice == '2':
        logger.info(f"Scraping data from the YouTube channel: {YOUTUBE_CHANNEL}")
        data = extract_yt_content(YOUTUBE_CHANNEL, YOUTUBE_SCROLL_LIMIT)
        if not data.empty:
            data.to_csv(yt_file_path, sep='|', index=False)
            csv_file_path = yt_file_path
            logger.success(f"Cleaned data saved to {yt_file_path}")
        break

    elif user_choice == '3':
        logger.info(f"Scraping data from the Instagram handle: {INSTAGRAM_HANDLE}")
        data = extract_ig_content(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, INSTAGRAM_HANDLE, INSTAGRAM_DATE_LIMIT)
        if not data.empty:
            data.to_csv(ig_file_path, sep='|', index=False)
            csv_file_path = ig_file_path
            logger.success(f"Cleaned data saved to {yt_file_path}")
        break

    else:
        print("Invalid choice! Please choose a number between 1 and 3.")
        print(" ")
