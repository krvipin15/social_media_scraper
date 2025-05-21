# ------------------------------------------ Importing Required Libraries --------------------------------------------------------------

import pandas as pd
from time import sleep
from datetime import datetime
from config import logger, driver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from deep_translator import GoogleTranslator
from selenium.webdriver.common.keys import Keys

# ---------------------------- Function to transalte all languages to English --------------------------------------------------------------------

def translate_text(txt: str) -> str:
    '''Translate the text in English from any other language using Google translator'''
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(txt)
        return translated
    except Exception as e:
        logger.error("Error in translating the text, returning the original text")
        return txt

# ------------------------------------------ Function to correct date format -----------------------------------------------------------------------

def fix_date_format(date_str: str) -> str:
    '''Convert time value into date value'''
    try:
        if 'hour' in date_str or 'hours' in date_str:
            hours = int(date_str.split(' ')[0])
            date = datetime.now() - timedelta(hours=hours)
        elif 'minute' in date_str or 'minutes' in date_str:
            minutes = int(date_str.split(' ')[0])
            date = datetime.now() - timedelta(minutes=minutes)
        elif 'second' in date_str or 'seconds' in date_str:
            seconds = int(date_str.split(' ')[0])
            date = datetime.now() - timedelta(seconds=seconds)
        elif 'day' in date_str or 'days' in date_str:
            days = int(date_str.split(' ')[0])
            date = datetime.now() - timedelta(days=days)
        elif 'week' in date_str or 'weeks' in date_str:
            weeks = int(date_str.split(' ')[0])
            date = datetime.now() - timedelta(weeks=weeks)
        elif 'month' in date_str or 'months' in date_str:
            months = int(date_str.split(' ')[0])
            date = datetime.now() - timedelta(days=months * 30)
        elif 'year' in date_str or 'years' in date_str:
            years = int(date_str.split(' ')[0])
            date = datetime.now() - timedelta(days=years * 365)
        return date.strftime('%Y-%m-%d')
    except Exception as e:
        logger.error("Error in date format conversion, returning original date")
        return date_str

# ------------------------------------------ Function to scrape youtube videos -----------------------------------------------------------------------

def extract_yt_content(channel_name: str, scroll_limit: int) -> pd.DataFrame:
    '''Scrapes data from YouTube channel'''
    videos_data = []
    driver.get(f'https://www.youtube.com/@{channel_name}/videos')
    logger.success("Succesfully reached the youtube channel webpage")
    sleep(2)

    # Scroll down the page to load videos
    logger.info("Scrolling down the webpage")
    for _ in range(scroll_limit):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        sleep(2)

    # Parse the page
    videos = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-rich-item-renderer')

    for indx, video in enumerate(videos):
        try:
            title_element = video.find_element(By.CSS_SELECTOR, 'a.yt-simple-endpoint.focus-on-expand.style-scope.ytd-rich-grid-media').get_attribute('title')
            title = translate_text(title_element)
            logger.success(f"[{indx+1}] Scraped the video: {title}")
            video_url_element = video.find_element(By.CSS_SELECTOR, 'a.yt-simple-endpoint.focus-on-expand.style-scope.ytd-rich-grid-media').get_attribute('href')
            metadata_items = video.find_elements(By.CSS_SELECTOR, 'span.inline-metadata-item.style-scope.ytd-video-meta-block')

            # Ensure metadata_items has two elements for views and posted_ago
            if len(metadata_items) >= 2:
                view_count = metadata_items[0].text.split(' views')[0]
                posted_ago = metadata_items[1].text
                posted_ago = fix_date_format(posted_ago)
            else:
                view_count = 'Unknown'
                posted_ago = 'Unknown'

            author_name = channel_name
            author_url = f'https://www.youtube.com/@{channel_name}/videos'

            img_url_element = video.find_element(By.CSS_SELECTOR, 'a.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail img')
            img_url = img_url_element.get_attribute('src')

            video_data = {
                'post': title,
                'video_url': video_url_element,
                'views': view_count,
                'posted_ago': posted_ago,
                'author': author_name,
                'author_link': author_url,
                'preview_image': img_url,
            }

            videos_data.append(video_data)
        except Exception as e:
            logger.error(f"Error processing video element: {e}")

    driver.quit()
    youtube_df = pd.DataFrame(videos_data)
    youtube_df.drop_duplicates(inplace=True)
    youtube_df['post'] = youtube_df['post'].str.replace('...', '', regex=False)
    logger.info(f"Total number of videos found from channel: {len(youtube_df)}")

    return youtube_df
