# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException

import common

class TopPage(object):
    def __init__(self, driver):
        self._driver = driver
        driver.get('https://mobile.twitter.com/session/new')

    def input_user_id(self, user_id):
        name = 'session[username_or_email]'
        elm = self._driver.find_element_by_name(name)
        elm.send_keys(user_id)
        return self

    def input_password(self, password):
        name = 'session[password]'
        elm = self._driver.find_element_by_name(name)
        elm.send_keys(password)
        return self

    def login(self):
        xpath = '//button[@type="submit"]'
        btn = self._driver.find_element_by_xpath(xpath)
        btn.click()
        return HomePage(self._driver)


class HomePage(object):
    def __init__(self, driver):
        self._driver = driver
        
    def to_input_tweet(self):
        try:
            xpath = '//span[contains(text(), "Sounds good")]/parent'
            button = self._driver.find_element_by_xpath(xpath)
            button.click()
        except NoSuchElementException:
            pass
        xpath = '//a[@href="/compose/tweet"]'
        link = self._driver.find_element_by_xpath(xpath)
        link.click()
        return TweetPage(self._driver)


class TweetPage(object):
    def __init__(self, driver):
        self._driver = driver

    def input_tweet(self, tweet):
        xpath = '//textarea[@data-testid="tweet-textarea"]'
        elm = self._driver.find_element_by_xpath(xpath)
        elm.send_keys(tweet)
        return self

    def tweet(self):
        xpath = '//button[@data-testid="tweet-button"]'
        elm = self._driver.find_element_by_xpath(xpath)
        elm.click()
        return self


def main():
    with common.xvfb():
        with common.firefox() as driver:
            TopPage(driver).input_user_id('XXXX')\
                           .input_password('XXXX')\
                           .login()\
                           .to_input_tweet()\
                           .input_tweet('テストですよ')\
                           .tweet()


if __name__ == '__main__':
    main()
