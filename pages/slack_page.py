import os
import pickle

from selenium.webdriver.common.by import By

from pages.base import WebPage
from pages.elements import WebElement, ManyWebElements


class SlackPage(WebPage):

    def __init__(self, web_driver, url='', email="своя почта)", password="свой пароль"):
        if not url:
            url = 'https://sf-team-new.slack.com/'
        super().__init__(web_driver, url)

        if os.path.isfile('../my_cookies.txt'):
            with open('../my_cookies.txt', 'rb') as cookiesfile:
                cookies = pickle.load(cookiesfile)
                for cookie in cookies:
                    web_driver.add_cookie(cookie)
            web_driver.refresh()
        else:
            web_driver.find_element(By.ID, 'email').send_keys(email)
            web_driver.find_element(By.ID, 'password').send_keys(password)
            web_driver.find_element(By.ID, 'signin_btn').click()
            with open('../my_cookies.txt', 'wb') as cookiesfile:
                pickle.dump(web_driver.get_cookies(), cookiesfile)
            web_driver.refresh()

    assert_id_side_bar = WebElement(id="channel_sidebar_group_expanded")
    btn_find = WebElement(xpath="//button[@aria-label='Поиск']")
    btn_find_input = WebElement(css_selector="div[aria-multiline='false'] p")
    btn_find_input_click = WebElement(css_selector="div[data-id$='0'] div[class*='entity']")
    message = WebElement(xpath="//div[@role='listitem']")
    btn_unwrap_list = ManyWebElements(xpath="//div[@class='c-search_message__attachment_body']/button[@aria-label='Развернуть']")
    btn_unwrap = WebElement(xpath="//div[@class='c-search_message__attachment_body']/button[@aria-label='Развернуть']")
    btn_unwrap_2 = WebElement(xpath="//button[contains(text(), 'Развернуть')]")
    body_message = WebElement(xpath="//div[@class='c-virtual_list__scroll_container c-search__results_container--virtualized']")
    all_messages = WebElement(xpath='//button[@id="messages"]/span[@class="c-tabs__tab_count"][@data-qa="tabs_item_render_count"]')
    btn_next_page = WebElement(xpath='//button[@aria-label="Следующая страница"]')
