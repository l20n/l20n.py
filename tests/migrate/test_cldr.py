# coding=utf8

import unittest
import sys

from l20n.migrate.cldr import get_plural_categories


class TestPluralCategories(unittest.TestCase):
    def __init__(self, *args):
        super(TestPluralCategories, self).__init__(*args)
        if sys.version_info < (3,0):
            self.assertRaisesRegex = self.assertRaisesRegexp


    def test_known_language(self):
        self.assertEqual(
            get_plural_categories('pl'),
            ('one', 'few', 'many', 'other')
        )

    def test_fallback_one(self):
        self.assertEqual(
            get_plural_categories('ga-IE'),
            ('one', 'two', 'few', 'many', 'other')
        )

    def test_fallback_two(self):
        self.assertEqual(
            get_plural_categories('ja-JP-mac'),
            ('other',)
        )

    def test_unknown_language(self):
        with self.assertRaisesRegex(RuntimeError, 'Unknown language'):
            get_plural_categories('i-default')
