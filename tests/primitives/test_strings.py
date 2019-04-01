from functools import reduce

from coverage.backunittest import TestCase

from botlang import BotlangSystem
from botlang.environment.primitives.strings.string_functions import string_similarity, \
    remove_same_words
from botlang.evaluation.values import Nil


class StringPrimitivesTestCase(TestCase):

    list_of_strings = [
        'Servicios Residenciales',
        'Servicios Móviles',
        'Interesado En Contratar O Renovar'
    ]

    def test_string_similarity(self):

        self.assertEqual(string_similarity('hola', 'hola'), 1)
        self.assertEqual(string_similarity('hola', 'HoLá'), 1)
        self.assertGreater(
            string_similarity('hola', 'holi'),
            string_similarity('hola', 'chao')
        )

    def test_remove_same_words(self):

        list_without_duplicates = remove_same_words(self.list_of_strings)
        self.assertSequenceEqual(
            [
                'Residenciales',
                'Móviles',
                'Interesado En Contratar O Renovar'
            ],
            list_without_duplicates
        )

    def get_similar_string(self, test, strings_list):

        botlang_list = '(list {})'.format(
            reduce(
                lambda acc, s: '{} "{}"'.format(acc, s),
                strings_list,
                ''
            )
        )
        return BotlangSystem.run(
            '(string-find-similar "%s" %s)' % (test, botlang_list)
        )

    def test_find_similar_string(self):

        self.assertEqual(
            self.get_similar_string('residencial', self.list_of_strings),
            self.list_of_strings[0]
        )
        self.assertEqual(
            self.get_similar_string('moviles', self.list_of_strings),
            self.list_of_strings[1]
        )
        self.assertEqual(
            self.get_similar_string('contratar', self.list_of_strings),
            self.list_of_strings[2]
        )
        self.assertEqual(
            self.get_similar_string('renovar', self.list_of_strings),
            self.list_of_strings[2]
        )
        self.assertEqual(
            self.get_similar_string(
                '1) servicios moviles', self.list_of_strings
            ),
            self.list_of_strings[1]
        )
        self.assertEqual(
            self.get_similar_string(
                'quiero contratar', self.list_of_strings
            ),
            self.list_of_strings[2]
        )
        self.assertEqual(
            self.get_similar_string(
                'me interesan los servicios moviles', self.list_of_strings
            ),
            self.list_of_strings[1]
        )
        self.assertEqual(
            self.get_similar_string(
                'me gustaria contratar un plan', self.list_of_strings
            ),
            self.list_of_strings[2]
        )
        self.assertEqual(
            self.get_similar_string(
                'necesito fibra optica residencial', self.list_of_strings
            ),
            self.list_of_strings[0]
        )

        self.assertEqual(
            self.get_similar_string('servicios', self.list_of_strings),
            Nil
        )
        self.assertEqual(
            self.get_similar_string('qwerty asdf', self.list_of_strings),
            Nil
        )
        self.assertEqual(
            self.get_similar_string(
                'no quiero na', self.list_of_strings
            ),
            Nil
        )
