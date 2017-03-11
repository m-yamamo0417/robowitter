# -*- coding: utf-8 -*-

import argparse
import configparser
import random
import re
import sys

import common
import twitter

class Generator(object):
    def __init__(self, config):
        self._config = config
        self._replace = re.compile('\{\{(.+)\}\}')

    def generate(self):
        head = self._config['common']['head']

        body = self.choose('messages')
        m = self._replace.search(body)
        while m:
            section = m.group(1)
            body = self._replace.sub(self.choose(section), body)
            m = self._replace.search(body)

        tail = self._config['common']['tail']

        max_body_length = 140 - len(head) - len(tail) - 2
        if len(body) > max_body_length:
            body = body[:max_body_length-3] + '...'
        
        return ' '.join([head, body, tail])

    def choose(self, section):
        keys = [key for key in self._config[section]]
        key = random.choice(keys)
        return self._config[section][key]


class ArgParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument('-u', '--userid')
        self.add_argument('-p', '--password')
        self.add_argument('inifile')


def main():
    argparser = ArgParser()
    args = argparser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.inifile)
    generator = Generator(config)
    tweet = generator.generate()

    with common.phantomjs() as driver:
        twitter.TopPage(driver)\
               .input_user_id(args.userid)\
               .input_password(args.password)\
               .login()\
               .to_input_tweet()\
               .input_tweet(tweet)\
               .tweet()


if __name__ == '__main__':
    main()
