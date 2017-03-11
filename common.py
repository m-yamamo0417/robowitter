# -*- coding: utf-8 -*-

# RoboLancer共通パッケージ

# -----------------------------------------------------------------------------
import logging
import os
import subprocess

from contextlib import contextmanager

from selenium import webdriver

# -----------------------------------------------------------------------------
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
@contextmanager
def phantomjs():
    driver = webdriver.PhantomJS('phantomjs',
                                 service_args=['--ssl-protocol=tlsv1'])
    yield driver
    driver.close()


@contextmanager
def firefox():
    """FireFoxオブジェクトをコンテキストマネージャーとして返す
    Usage:
        with firefox() as driver:
            ...
    """
    driver = webdriver.Firefox()
    yield driver
    driver.close()

@contextmanager
def xvfb():
    """XVfbを起動します
    Usage:
        with xvfb():
            ...
    """
    display_no = ':9'
    proc = subprocess.Popen(['Xvfb', '-ac', display_no])
    os.environ['DISPLAY'] = display_no

    yield

    proc.kill()
    os.environ.pop('DISPLAY')


# -----------------------------------------------------------------------------
class ClowdSourcing(object):
    def __init__(self, driver, user, password):
        self._driver   = driver
        self._user     = user
        self._password = password

    def __enter__(self):
        logger.info('login')
        self.login(self._driver, self._user, self._password)

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.warn(exc_value)

        logger.info('logout')
        self.logout(self._driver)

    def login(self, driver, user, password):
        raise NotImplementedError()

    def logout(self, driver):
        raise NotImplementedError()

class Lancers(ClowdSourcing):
    """
    Usage:
        with Lancers(driver, 'user@example.com', 'password') as lancers:
            ...
    """
    def __init__(self, driver, user, password):
        super().__init__(driver, user, password)

    def login(self, driver, user, password):
        # ログイン画面を表示する
        driver.get('http://www.lancers.jp/user/login')

        # 入力フォームを取得する
        elm_email     = driver.find_element_by_id('UserEmail')
        elm_password  = driver.find_element_by_id('UserPassword')
        elm_autologin = driver.find_element_by_id('UserAutoLogin')
        elm_form      = driver.find_element_by_name('login')

        # 必要なパラメータを入力する
        elm_email.send_keys(user)
        elm_password.send_keys(password)
        if elm_autologin.is_selected():
            elm_autologin.click()

        # 入力内容を送信する
        elm_form.submit()

    def logout(self, driver):
        driver.get('http://www.lancers.jp/user/logout?ref=header_menu')
            
