from time import sleep
import datetime
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from pages.slack_page import SlackPage


def test_slack(web_browser):
    page = SlackPage(web_browser)
    page.wait_page_loaded(sleep_time=10)

    assert page.assert_id_side_bar.is_presented()
    page.btn_find.click()
    page.btn_find_input.send_keys("development / lms_beta_test")
    page.btn_find_input_click.click()
    page.wait_page_loaded()

    messages_id_list = []
    messages_in_page = []

    messages_all = []

    while True:
        messages_list = web_browser.find_elements(By.CSS_SELECTOR, "div[id^='messages']")
        messages_temp_id_list = []
        for i in range(len(messages_list)):
            message_id = (messages_list[i].get_attribute("id"))
            if message_id not in messages_id_list:
                messages_id_list.append(message_id)
                messages_temp_id_list.append(message_id)
        if not messages_temp_id_list:
            messages_all += messages_in_page
            break

        for id in messages_temp_id_list:
            try:
                message = web_browser.find_element(By.CSS_SELECTOR, "div[id='{id}']".format(id=id))
            except NoSuchElementException:
                print(id)
                print(messages_id_list)
                print(messages_temp_id_list)
                break
            ActionChains(web_browser) \
                .scroll_to_element(message) \
                .perform()

            try:
                button_unwrap = web_browser.find_element(By.CSS_SELECTOR,
                                                         "div[id='{id}'] button[aria-label='Развернуть']".format(
                                                             id=id))
                button_unwrap.click()
                sleep(0.3)
            except NoSuchElementException:
                pass

            try:
                button_unwrap_2 = web_browser.find_element(By.CSS_SELECTOR,
                                                           "div[id='{id}'] button[type='button'][class='c-link--button c-message_attachment__text_expander']".format(
                                                               id=id))
                button_unwrap_2.click()
                sleep(0.3)
            except NoSuchElementException:
                pass

            message = web_browser.find_element(By.CSS_SELECTOR, "div[id='{id}']".format(id=id))
            ActionChains(web_browser) \
                .scroll_to_element(message) \
                .perform()

            if message not in messages_in_page:
                message = message.text.replace(",", "")
                messages_in_page.append(message.split("\n"))
        try:
            if len(messages_in_page) == 20:
                page.btn_next_page.click()
                page.wait_page_loaded()
                messages_all += messages_in_page
                messages_in_page.clear()
        except AttributeError:
            pass

    del messages_all[0]

    for item in messages_all:
        if item[3] == 'Посмотреть в канале':
            del item[3]

    for item in messages_all:
        print(item)
    data = datetime.datetime.now().strftime('%H_%M_%S')
    with open(f"bug{data}.csv", "a") as file:
        print('Тема', 'Автор:', 'Описание:', 'Ссылка:', 'Скриншоты:', sep="\\", file=file)
        for item in messages_all:
            for i in range(1, len(item)):
                ceil = item[i]
                if ceil.find("[development / lms_beta_test]") != -1:
                    print(ceil[ceil.find(']') + 1:], end="\\", file=file)
                if item[i - 1] in ['Автор:', 'Описание:']:
                    print(ceil, end="\\", file=file)
                if item[i - 1] in ['Ссылка:', 'Скриншоты:']:
                    print(ceil[ceil.find('>') + 1:], end="\\", file=file)
                if i == len(item) - 1 and ceil == 'Скриншоты:':
                    print("Скрина нет", end="\\", file=file)
            print("\n", file=file)
    web_browser.quit()
