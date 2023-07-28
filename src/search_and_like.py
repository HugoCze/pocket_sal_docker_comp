import os
import time 
import argparse
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, ElementNotInteractableException, StaleElementReferenceException, TimeoutException,ElementClickInterceptedException

date_time = datetime.datetime.now()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-features=DefaultPassthroughCommandDecoder")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--ignore-ssl-errors=yes")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("----headless")
# chrome_options.headless = True

driver = webdriver.Chrome(options=chrome_options)

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
            print("got home page")
            self.terms(path, comment, like_dislikle)
            time.sleep(5)
        except ignored_exceptions:
            print(f"Search_And_Like - failed to get homePage - refresh and terms")
            self.terms(path, comment, like_dislikle)
    
    def terms(self, path, comment, like_dislikle):
        print("Terms and conditions starting...")
        try:
            self.click("/html/body/div[3]/div/div[2]/div[3]/div/button[2]", "clicked accept terms button")
            self.search_comment(path, comment, like_dislikle)
        except ignored_exceptions:
            print(f"terms - Terms and conditions not found - searching comment")
            self.search_comment(path, comment, like_dislikle)
    
    def click(self, xpath, call_indication):
        button_location = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button_location)
        print(f"click - clicking given xpath: {xpath} - {call_indication}")

    def search_comment(self, path, comment):
        time.sleep(3)
        print(f"search_comment - searching for comment - CURRENT PAGE IS: {self.CURRENT_PAGE}",)
        for i in range(0, 34):
            try:
                possible_comment_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[2]'
                comment_location = driver.find_element(By.XPATH, possible_comment_xp)
                comment_text = comment_location.get_attribute('innerHTML')
                print(comment_text.encode("utf-8"))
                if comment_text.strip() == comment.strip():
                    time.sleep(10)
                    like_button = possible_comment_xp[:-6]
                    like_button_xp = like_button + "div[1]/div[2]/div/button[1]"
                    print("got the like butt xpath")
                    time.sleep(3)
                    self.click(like_button_xp, "search_comment - called click like button from comment searching")
                    self.CURRENT_PAGE = 1
                    self.COMMENT_BUCKET = []
                    return
            except ignored_exceptions:
                pass
        else:
            print("CALLING SEARCH NEXT FROM SEARCH COMMENT")
            self.search_next(path, comment)
    
    def search_next(self, path, comment):
        print("search_next - searching the next button")
        for i in range(1, 42):
            for j in range(2,4):
                try:
                    next_button_xp = f'//*[@id="page_content"]/div[1]/div/div[3]/div/div/div/div/div[{i}]/div/div[{j}]/div[3]/div/div'
                    button_action = driver.find_element(By.XPATH, next_button_xp)
                    button_possible_text = button_action.get_attribute('innerHTML')
                    if button_possible_text == "Następna strona":
                        print("search_next - got the next button")
                        self.click(next_button_xp, "search_next - clicked the next button")
                        self.CURRENT_PAGE += 1
                        self.search_comment(path, comment)
                        return
                except ignored_exceptions:
                    pass
    
    def main(self, path, comment, like_dislikle):
        print(f" \n \n main - here we are at main. Calling get_homePage. Like/dislike == {like_dislikle}")
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
        print(f"Time of looking the comment is equal to: {total_time} ")
        print(f"Counter: {SAL.PROCCESS_COUNTER} ")