# ------------------------------------------ Importing Required Libraries ---------------------------------------------------------------------

import pandas as pd
from time import sleep
from datetime import datetime
from config import logger, driver
from selenium.webdriver.common.by import By
from deep_translator import GoogleTranslator
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----------------------------------------------- Xpath variables ------------------------------------------------------------------------------

url_xpath = "//div[@class='x1lliihq x1n2onr6 xh8yej3 x4gyw5p x11i5rnm x1ntc13c x9i3mqj x2pgyrj']//a"
video_xpath = "//div[@class='x5yr21d x1uhb9sk xh8yej3']//video"
img_xpath = "//div[@class='x1lliihq x1n2onr6 xh8yej3 x4gyw5p x11i5rnm x1ntc13c x9i3mqj x2pgyrj']//div//div//img"
date_xpath = '//span[@class="x1lliihq x1plvlek xryxfnj x1n2onr6 x1ji0vk5 x18bv5gf x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1fhwpqd xo1l8bm x1roi4f4 x1s3etm8 x676frb x10wh9bi x1wdrske x8viiok x18hxmgj"]//time'
likes_xpath = '//span[@class="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"]//span'
desc_xpath = '//span[@class="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"]'

# ---------------------------------- Function to transalte all languages to English -------------------------------------------------------------

def translate_text(txt: str) -> str:
    '''Translate the text in English from any other language using Google translator'''
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(txt)
        return translated
    except Exception as e:
        logger.error("Error in translating the text, returning the original text")
        return txt

# ------------------------------------------ Function to scrape posts -----------------------------------------------------------------------

def extract_ig_content(username: str, password: str, instagram_handle: str, date_limit: datetime):
    '''Scrape the data from instagram handle'''
    logger.info("Proceeding to login to the Instagram account")
    driver.get("https://instagram.com/")
    sleep(3)

    # Find and input the username
    try:
        username_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
        username_input.send_keys(username)
        sleep(1)

        # Find and input the password
        password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        sleep(5)
    except Exception as e:
        logger.error("""Login failed! Check credentials or website structure.
                     Traceback: {e}""")
        driver.quit()

    logger.info("Successfully logged in")
    logger.info(f"Proceeding to scrape posts from @{instagram_handle} for the date range {date_limit.strftime('%d %B %Y')} to {datetime.now().strftime('%d %B %Y')}")
    driver.get(f"https://instagram.com/{instagram_handle}")
    sleep(2.5)

    stop_scraping = False
    instagram_data = []    # Store all the required data
    visited_links = set()  # Store all the previous urls

    while not stop_scraping:
        # Scrolling down the webpage
        driver.execute_script("window.scrollBy(0, 1000);")
        sleep(2.5)

        # Extract the post urls
        urls = driver.find_elements(By.XPATH, url_xpath)
        post_links = [url.get_attribute("href") for url in urls if url.get_attribute("href") not in visited_links]

        if not post_links:
            break

        for link in post_links:
            logger.success(f"Scraped post: {link}")
            visited_links.add(link)
            driver.execute_script(f"window.open('{link}', '_blank');")
            driver.switch_to.window(driver.window_handles[1])
            sleep(5)

            try:
                try:
                    media = driver.find_element(By.XPATH, video_xpath).get_attribute("src").removeprefix("blob:")
                except:
                    media = driver.find_element(By.XPATH, img_xpath).get_attribute("src")
                _date = driver.find_element(By.XPATH, date_xpath).get_attribute("datetime")
                _date = datetime.strptime(_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                likes = driver.find_element(By.XPATH, likes_xpath).text.replace(',', '')
                desc = driver.find_element(By.XPATH, desc_xpath).text
                desc = translate_text(desc)

                if _date < date_limit:
                    logger.info(f"Reached posts older than {date_limit.strftime('%d %B %Y')}. Stopping the scraper.")
                    stop_scraping = True
                    break

                instagram_data.append({
                    "date": _date.strftime("%Y-%m-%d"),
                    "description": desc,
                    "media": media,
                    "likes": likes,
                    "url": link
                })
            except Exception as e:
                logger.error(f"Error scraping post at {link}: {e}")

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            sleep(2)

        if stop_scraping:
            break

    driver.quit()
    instagram_df = pd.DataFrame(instagram_data)
    instagram_df.drop_duplicates(inplace=True)
    logger.info(f"Total number of posts found: {len(instagram_df)}")

    return instagram_df
