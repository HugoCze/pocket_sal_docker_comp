import os
import time 
import logging
import argparse
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, ElementNotInteractableException, StaleElementReferenceException, TimeoutException,ElementClickInterceptedException
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler


class MaxRowsFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', max_rows=50, encoding=None, delay=0):
        super().__init__(filename, mode, encoding, delay)
        self.max_rows = max_rows
        self.rows_logged = 0

    def emit(self, record):
        # Check if the number of logged rows exceeds the limit
        if self.rows_logged >= self.max_rows:
            # If it exceeds, truncate the file and reset the row count
            self.stream.truncate(0)
            self.rows_logged = 0

        # Call the parent's emit method to log the record
        super().emit(record)
        self.rows_logged += 1

# Create a logger and add the custom handler
logger = logging.getLogger('app_logger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Use MaxRowsFileHandler instead of FileHandler
handler = MaxRowsFileHandler(filename='app.log', max_rows=50)
handler.setFormatter(formatter)
logger.addHandler(handler)

date_time = datetime.datetime.now()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-features=DefaultPassthroughCommandDecoder")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--ignore-ssl-errors=yes")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("----headless")

# FOR EC2
chrome_driver_path = "/usr/local/bin/chromedriver/chromedriver"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
# ONLY FOR LOCAL TESTS
# driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(5)


ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException,\
     TimeoutException, ElementClickInterceptedException, InvalidSessionIdException)


Chrome_wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)


class Search_And_Like:

    CURRENT_DRIVER = ""
    PROCCESS_COUNTER = 0
    COMMENT_BUCKET = []
    BUCKET_STATUS = False
    FIRST_FIRST_PAGE_COMMENT = ""
    CURRENT_PAGE = 1

    
    def get_homePage(self, path, comment, like_dislikle):
        homepage = "https://www.pudelek.pl/" + path
        try:
            driver.get(homepage)
            logger.info(f"got home page: {homepage}")
            self.terms(path, comment, like_dislikle)
            time.sleep(5)
        except ignored_exceptions:
            logger.info(f"Search_And_Like - failed to get homePage - refresh and terms")
            self.terms(path, comment, like_dislikle)
    
    def terms(self, path, comment, like_dislikle):
        logger.info("Terms and conditions starting...")
        try:
            self.click("/html/body/div[3]/div/div[2]/div[3]/div/button[2]", "clicked accept terms button")
            self.search_comment(path, comment, like_dislikle)
        except ignored_exceptions:
            logger.info(f"terms - Terms and conditions not found - searching comment")
            self.search_comment(path, comment, like_dislikle)
    
    def click(self, xpath, call_indication):
        button_location = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button_location)
        logger.info(f"click - clicking given xpath: {xpath} - {call_indication}")

    def search_comment(self, path, comment1, like_dislikle):
        time.sleep(3)
        logger.info(f"comment1: {comment1}")
        logger.info(f"search_comment - searching for comment - CURRENT PAGE IS: {self.CURRENT_PAGE}",)
        for i in range(0, 34):
            try:
                possible_comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[2]'
                comment_location = driver.find_element(By.XPATH, possible_comment_xp)
                comment_text = comment_location.get_attribute('innerHTML')
                # print(comment_text)
                # print(comment1)
                logger.info(comment_text.encode("utf-8"))
                if comment_text.strip().replace('\n', ' ') == comment1.strip().replace('\n', ' '):
                    time.sleep(10)
                    like_button = possible_comment_xp[:-6]
                    like_button_xp = like_button + "div[1]/div[2]/div/button[1]"
                    dis_like_button_xp = like_button + "div[1]/div[2]/div/button[2]"
                    time.sleep(3)
                    if like_dislikle == "like":
                        self.click(like_button_xp, "search_comment - called click like button from comment searching")
                    elif like_dislikle == "dislike":
                        self.click(dis_like_button_xp, "search_comment - called click dislike button from comment searching")
                    self.CURRENT_PAGE = 1
                    self.COMMENT_BUCKET = []
                    return
            except ignored_exceptions:
                pass
        else:
            logger.info("CALLING SEARCH NEXT FROM SEARCH COMMENT")
            self.search_next(path, comment1, like_dislikle)
    
    def search_next(self, path, comment, like_dislikle):
        logger.info("search_next - searching the next button")
        for i in range(1, 42):
            for j in range(2,4):
                try:
                    next_button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div'
                    button_action = driver.find_element(By.XPATH, next_button_xp)
                    button_possible_text = button_action.get_attribute('innerHTML')
                    if button_possible_text == "Następna strona":
                        logger.info("search_next - got the next button")
                        self.click(next_button_xp, "search_next - clicked the next button")
                        self.CURRENT_PAGE += 1
                        self.search_comment(path, comment, like_dislikle)
                        return
                except ignored_exceptions:
                    pass
    
    def main(self, path, comment, like_dislikle):
        logger.info(f" \n \n main - here we are at main. Calling get_homePage. Like/dislike == {like_dislikle}")
        self.get_homePage(path, comment, like_dislikle)

SAL = Search_And_Like()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--article', type=str, help='An integer argument')
    parser.add_argument('--comment', type=str, help='An integer argument')
    parser.add_argument('--like_dislike', type=str, help='An integer argument')
    args = parser.parse_args()

    while True:
        SAL.PROCCESS_COUNTER += 1 
        start_time = time.time()
        SAL.main(args.article, args.comment, args.like_dislike)
        end_time = time.time()
        total_time = end_time - start_time
        logger.info(f"Time of looking the comment is equal to: {total_time} ")
        logger.info(f"Counter: {SAL.PROCCESS_COUNTER} ")



# python3 search_and_like.py --article "https://www.pudelek.pl/kinga-rusin-komentuje-tragiczny-pozar-na-rodos-ewakuowano-wszystkich-mieszkancow-miejscowosci-sasiadujacej-z-nasza-wioska-6923733386107872a?fbclid=IwAR0eb8JgpF4vPFCyvRNT_5kqnhePmDNu1EHBWo_l0fd7fyQR_TFwZNDklJc"  --comment "A ja uważam, ze Kinga takimi postami się zwyczajnie promuje. To jest ludzka tragedia, a dla pani pretekst żeby wrzucić swoje zdjęcie. Taki jest zreszta cały instagram. Niewazne jak poważny post, każdy obudowany jest selfikiem. Inna sprawa, że nagle każdy celebryta mieszka w Grecji, zna każda uliczkę i robi zakupy w lokalnych sklepach. Grecja jest popularnym kierunkiem, nie tylko wy tam jeździcie, drodzy celebryci ;)" --like_dislike "dislike"
# python3 search_and_like.py --article "https://www.pudelek.pl/kinga-rusin-komentuje-tragiczny-pozar-na-rodos-ewakuowano-wszystkich-mieszkancow-miejscowosci-sasiadujacej-z-nasza-wioska-6923733386107872a?fbclid=IwAR0eb8JgpF4vPFCyvRNT_5kqnhePmDNu1EHBWo_l0fd7fyQR_TFwZNDklJc" --comment "kogo obchodzi co myśli Rusinowa.. żenada.. żaden autorytet i szkoda czasu na nią... niech wraca sobie na te Malediwy czy gdzie ona tam lata.." --like_dislike "dislike"