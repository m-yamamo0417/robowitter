# -*- coding: utf-8 -*-

import unittest as ut
import unittest.mock as utm

import randomtweet

class GeneratorTest(ut.TestCase):
    def test_generate(self):
        with utm.patch('random.choice', return_value='1'):
            config = {'common': {'head': 'HEADLINE',
                                 'tail': 'TAIL'},
                      'messages': {'1': '1234567890' * 15}}
            generator = randomtweet.Generator(config)
            self.assertEqual('HEADLINE ' +                                #   9chars
                             '1234567890123456789012345678901234567890' + #  49chars
                             '1234567890123456789012345678901234567890' + #  89chars
                             '1234567890123456789012345678901234567890' + # 129chars
                             '123...' +                                   # 135chars
                             ' TAIL',                                     # 140chars
                             generator.generate())

            config = {'common': {'head': 'HEADLINE',
                                 'tail': 'TAIL'},
                      'messages': {'1': '{{messages1}}'},
                      'messages1': {'1': 'message'}}
            generator = randomtweet.Generator(config)
            self.assertEqual('HEADLINE message TAIL', generator.generate())

    def test_choose(self):
        with utm.patch('random.choice', return_value='1'):
            config = {'messages': {'1': '1234567890'}}
            generator = randomtweet.Generator(config)
            self.assertEqual('1234567890', generator.choose('messages'))


class ArgParserTest(ut.TestCase):
    def test_parse(self):
        args = ['userid', 'password', 'inifile.ini']
        parser = randomtweet.ArgParser()
        args = parser.parse_args(args)
        self.assertEqual('userid', args.userid)
        self.assertEqual('password', args.password)
        self.assertEqual('inifile.ini', args.inifile)
