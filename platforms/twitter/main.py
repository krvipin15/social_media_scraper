#------------------------------------------ Importing Required Libraries --------------------------------------------------------------

import pandas as pd
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from config import logger, driver
from selenium.webdriver.common.by import By
from deep_translator import GoogleTranslator
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#----------------------------------- Function to transalte all languages to English ---------------------------------------------------------

def translate_text(txt: str) -> str:
    '''Translate the text in English from any other language using Google translator'''
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(txt)
        return translated
    except Exception as e:
        logger.error("Error in translating the text, returning the original text")
        return txt

#------------------------------------------ Function to scrape tweets -----------------------------------------------------------------------

def extract_tw_content(username: str, password: str, twitter_handle: str, date_limit: datetime) -> pd.DataFrame:
    '''Scrape data from twitter handle'''
    logger.info("Proceeding to login to the Twitter account")
    driver.get("https://x.com/i/flow/login")
    sleep(3)

    try:
        # Find and input the username
        username_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
        username_input.send_keys(username)
        username_input.send_keys(Keys.ENTER)
        sleep(1)

        # Find and input the password
        password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        sleep(5)
    except:
        logger.error("Login failed! Check credentials or website structure.")
        driver.quit()

    logger.success("Successfully logged in")
    logger.info(f"Proceeding to scrape tweets from @{twitter_handle} for the date range {date_limit.strftime('%d %B %Y')} to {datetime.now().strftime('%d %B %Y')}")
    driver.get(f"https://x.com/{twitter_handle}")
    sleep(2.5)

    stop_scraping = False
    previous_tweets = set()   # Store the previous tweets to compare with new tweets
    tweet_data = []           # Store all the required tweet data

    while True:
        # Scrolling down the webpage
        driver.execute_script("window.scrollBy(0, 1000);")
        sleep(2.5)

        # Parse the page and extract tweets
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tweets = soup.find_all('article', {'data-testid': 'tweet'})

        for tweet in tweets:
            if tweet in previous_tweets:
                continue

            # Extracting all the data
            url = tweet.find('a', {"class": "css-146c3p1 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-xoduu5 r-1q142lx r-1w6e6rj r-9aw3ui r-3s2u2q r-1loqt21"})['href']
            url = f"https://x.com{url}"
            logger.success(f"Scraped tweet: {url}")
            try:
                imgurl = tweet.find('div', {'data-testid': 'tweetPhoto'}).find('img').get('src')
            except:
                imgurl = "None"
            post = tweet.find('div', {'data-testid': 'tweetText'}).text.replace("…", "").strip()
            name = tweet.find('div', {'data-testid': 'User-Name'}).find('span').text.strip()
            handle, _ = tweet.find('div', {"class": "css-175oi2r r-18u37iz r-1wbh5a2 r-1ez5h0i"}).text.split('·')
            handle = handle.strip()
            date = tweet.find('div', {'data-testid': 'User-Name'}).find('time').get("datetime")
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
            interactions = tweet.find_all('span', {'data-testid': 'app-text-transition-container'})
            comments = interactions[0].text.strip() if len(interactions) > 0 else "0"
            retweets = interactions[1].text.strip() if len(interactions) > 1 else "0"
            likes = interactions[2].text.strip() if len(interactions) > 2 else "0"
            views = interactions[3].text.strip() if len(interactions) > 3 else "0"

            # Stop if the tweet is older than date_limit
            if date < date_limit:
                logger.info(f"Reached tweets older than {date_limit.strftime('%d %B %Y')}. Stopping the scraper.")
                # stop_scraping = True
                break

            tweet_data.append({
                "name": name,
                "handle": handle,
                "imgurl": imgurl,
                "retweets": retweets,
                "likes": likes,
                "comments": comments,
                "views": views,
                "url": url,
                "post": post,
                "date": date
            })

            previous_tweets.add(tweet)
        if stop_scraping:
            break

    driver.quit()

    tweet_df = pd.DataFrame(tweet_data)
    tweet_df.drop_duplicates(inplace=True)
    logger.info(f"Total number of tweets found: {len(tweet_df)}")

    return tweet_df
