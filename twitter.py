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
        xpath = '//input[@type="submit"]'
        btn = self._driver.find_element_by_xpath(xpath)
        btn.click()
        return HomePage(self._driver)


class HomePage(object):
    def __init__(self, driver):
        self._driver = driver
        
    def to_input_tweet(self):
        xpath = '//button[@data-testid="Button"]'
        buttons = self._driver.find_elements_by_xpath(xpath)
        if len(buttons) == 2:
            button[0].click()
        xpath = '//a[@href="/compose/tweet"]'
        link = self._driver.find_element_by_xpath(xpath)
        link.click()
        return TweetPage(self._driver)


class TweetPage(object):
    def __init__(self, driver):
        self._driver = driver

    def input_tweet(self, tweet):
        xpath = '//textarea[@name="tweet[text]"]'
        elm = self._driver.find_element_by_xpath(xpath)
        elm.send_keys(tweet)
        return self

    def tweet(self):
        xpath = '//input[@type="submit"]'
        elm = self._driver.find_element_by_xpath(xpath)
        elm.click()
        return self


def main():
    with common.xvfb():
        with common.firefox() as driver:
            TopPage(driver).input_user_id('PiRobowitter')\
                           .input_password('robo.m.yamamo.tter')\
                           .login()\
                           .to_input_tweet()\
                           .input_tweet('テストですよ')\
                           .tweet()


if __name__ == '__main__':
    main()
