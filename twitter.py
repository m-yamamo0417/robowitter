# -*- coding: utf-8 -*-

import common

class TopPage(object):
    def __init__(self, driver):
        self._driver = driver
        driver.get('https://mobile.twitter.com/session/new')

    def input_user_id(self, user_id):
        _id = 'session[username_or_email]'
        elm = self._driver.find_element_by_id(_id)
        elm.send_keys(user_id)
        return self

    def input_password(self, password):
        _id = 'session[password]'
        elm = self._driver.find_element_by_id(_id)
        elm.send_keys(password)
        return self

    def login(self):
        btn = self._driver.find_element_by_name('commit')
        btn.click()
        return HomePage(self._driver)


class HomePage(object):
    def __init__(self, driver):
        self._driver = driver
        
    def to_input_tweet(self):
        xpath = '//a[@href="/compose/tweet"]'
        link = self._driver.find_element_by_xpath(xpath)
        link.click()
        return TweetPage(self._driver)


class TweetPage(object):
    def __init__(self, driver):
        self._driver = driver

    def input_tweet(self, tweet):
        elm = self._driver.find_element_by_name('tweet[text]')
        elm.send_keys(tweet)
        return self

    def tweet(self):
        elm = self._driver.find_element_by_name('commit')
        elm.click()
        return self


def main():
    with common.phantomjs() as driver:
        TopPage(driver).input_user_id('PiRobowitter')\
                       .input_password('robo.m.yamamo.tter')\
                       .login()\
                       .to_input_tweet()\
                       .input_tweet('テストですよ')\
                       .tweet()


if __name__ == '__main__':
    main()
