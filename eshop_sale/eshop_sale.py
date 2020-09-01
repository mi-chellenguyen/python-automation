from fbchat import Client
from fbchat.models import *

from decouple import config
from selenium import webdriver
import time
import schedule

# This small script scans the Nintendo eShop website once a day at noon
# to determine if the specifc game the user is searching for is on sale.
# If the item happens to be on sale, then the program will send a
# Facebook message to notify the user.

def check_for_sale(link,webdriver_path,email,password):
    """
    Browse Nintendo eShop and determine if game is on sale.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    driver = webdriver.Chrome(executable_path= r'{}'.format(webdriver_path),options=options)
    driver.get(link)
    time.sleep(5)
    
    game_title = driver.find_element_by_css_selector('h1.h2.game-title').text
    sale_price = driver.find_element_by_css_selector('span.h2.sale-price').text.strip()
    if sale_price:
        print("The game", game_title, "is on sale for", sale_price)
        send_fb_msg(email,password,game_title,sale_price)
    else:
        print("game not on sale right now")
    driver.close()
    driver.quit()

def send_fb_msg(email,password,game_title,sale_price):
    """
    Log into Facebook and sends the user a message to notify 
    if game price is currently reduced.
    """
    # Log the user in on Facebook
    client = Client(EMAIL, PASSWORD)

    if not client.isLoggedIn():
        client.loginClient(EMAIL, PASSWORD)

    # Send a message to user
    msg = "The game " + game_title + " is currently on sale for " + sale_price
    client.send(Message(text=msg), thread_id=client.uid, thread_type=ThreadType.USER)

    # Log the user out
    client.logout()


if __name__ == "__main__":
    WEBSITE_LINK = config('WEB_LINK')
    EMAIL = config('EMAIL')
    PASSWORD =  config('PASSWORD')
    WEBDRIVER_PATH = config('WEBDRIVER_PATH')

    check_for_sale(WEBSITE_LINK,WEBDRIVER_PATH,EMAIL,PASSWORD)
    # schedule.every().day.at("12:00").do(check_for_sale(WEBSITE_LINK,WEBDRIVER_PATH,EMAIL,PASSWORD))
    # schedule.every().minute.at(":05").do(check_for_sale(WEBSITE_LINK,WEBDRIVER_PATH,EMAIL,PASSWORD))
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

