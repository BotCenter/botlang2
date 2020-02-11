import json
from unittest import TestCase

from botlang import BotlangSystem
from botlang.environment.primitives.collections import get_value_in_dict
from botlang.evaluation.values import Nil


class CollectionsTestCase(TestCase):

    def test_get_value_in_dict(self):
        the_dict = {'datos': {'mensajes': {'user': {'text': 'Jose'}}}}

        result_value = get_value_in_dict(the_dict, 'datos.mensajes.user.text')
        expected_value = 'Jose'
        self.assertEqual(expected_value, result_value)

        result_value = get_value_in_dict(the_dict, 'datos.mensajes')
        expected_value = {'user': {'text': 'Jose'}}

        self.assertEqual(expected_value, result_value)

        result_value = get_value_in_dict({'dict': {}}, 'dict')
        expected_value = {}

        self.assertEqual(expected_value, result_value)

        with self.assertRaises(KeyError):
            get_value_in_dict(the_dict, 'texto')
        with self.assertRaises(KeyError):
            get_value_in_dict({}, 'texto')
        with self.assertRaises(KeyError):
            get_value_in_dict({}, '')

    def test_get(self):
        value = BotlangSystem.run("""
            (define a_dict (make-dict))
            (put! a_dict "uno" 1)
            (get a_dict "uno")
        """)
        self.assertEqual(1, value)

        value = BotlangSystem.run("""
            (define a_dict (make-dict))
            (define another_dict (make-dict))
            (put! another_dict "uno" 1)
            (put! a_dict "another_dict" another_dict)
            (get a_dict "another_dict.uno")
        """)
        self.assertEqual(1, value)

        value = BotlangSystem.run("""
            (define a_dict (make-dict))
            (define another_dict (make-dict))
            (put! another_dict "uno" 1)
            (put! another_dict "dos" 2)
            (put! a_dict "another_dict" another_dict)
            (get-or-nil a_dict "another_dict.tres")
        """)
        self.assertEqual(Nil, value)

        value = BotlangSystem.run("""
            (define a_list (list "hola" "como" "estas"))
            (get a_list 2)
        """)
        self.assertEqual("estas", value)

        value = BotlangSystem.run("""
            (define a_list (list "hola" "como" "estas"))
            (get-or-nil a_list 3)
        """)
        self.assertEqual(Nil, value)

    def test_get_default(self):

        value = BotlangSystem.run("""
            (define a_dict (make-dict))
            (get a_dict "uno" 1)
        """)
        self.assertEqual(1, value)

        value = BotlangSystem.run("""
            (define a_dict (make-dict))
            (define another_dict (make-dict))
            (put! another_dict "uno" 1)
            (put! another_dict "dos" 2)
            (put! a_dict "another_dict" another_dict)
            (get a_dict "another_dict.tres" nil)
        """)
        self.assertEqual(value, Nil)

        value = BotlangSystem.run("""
            (define a_list (list "hola" "como" "estas"))
            (get a_list 10 "chao")
        """)
        self.assertEqual("chao", value)

    def test_key_exists(self):

        value = BotlangSystem.run("""
        (define a (make-dict (list (cons "a" "b"))))
        (exists? a "a")
        """)
        self.assertTrue(value)

        value = BotlangSystem.run("""
        (define d (make-dict (list (cons "a" "b"))))
        (exists? d "b")
        """)
        self.assertFalse(value)

    def test_extend(self):

        value = BotlangSystem.run('(extend (list 1 2 3) (list 4 5 6))')
        self.assertSequenceEqual(value, [1, 2, 3, 4, 5, 6])

        value = BotlangSystem.run('(extend (list 1 2 3) 4)')
        self.assertSequenceEqual(value, [1, 2, 3, 4])

    def test_find(self):

        value = BotlangSystem.run('(find (fun (e) (> e 3)) (list 1 2 3 4 5))')
        self.assertEqual(value, 4)

        value = BotlangSystem.run('(find (fun (e) (> e 5)) (list 1 2 3 4 5))')
        self.assertEqual(value, Nil)

    def test_empty_list(self):

        value = BotlangSystem.run('(empty? (list))')
        self.assertTrue(value)

        value = BotlangSystem.run('(empty? (list 1))')
        self.assertFalse(value)

        value = BotlangSystem.run('(empty? (list 1 2 3 4))')
        self.assertFalse(value)

        value = BotlangSystem.run('(not-empty? (list))')
        self.assertFalse(value)

        value = BotlangSystem.run('(not-empty? (list 1))')
        self.assertTrue(value)

        value = BotlangSystem.run('(not-empty? (list 1 2 3 4))')
        self.assertTrue(value)

    def test_split_n(self):

        list1, list2 = BotlangSystem.run('(split-n (list 1 2 3 4 5 6) 2)')
        self.assertSequenceEqual(list1, [1, 2])
        self.assertSequenceEqual(list2, [3, 4, 5, 6])

        list1, list2 = BotlangSystem.run('(split-n (list 1 2 3 4 5 6) 10)')
        self.assertSequenceEqual(list1, [1, 2, 3, 4, 5, 6])
        self.assertSequenceEqual(list2, [])

        list1, list2 = BotlangSystem.run('(split-n (list 1 2 3 4 5 6) 0)')
        self.assertSequenceEqual(list1, [])
        self.assertSequenceEqual(list2, [1, 2, 3, 4, 5, 6])

        list1, list2 = BotlangSystem.run('(split-n (list) 5)')
        self.assertSequenceEqual(list1, [])
        self.assertSequenceEqual(list2, [])

    def test_to_json(self):

        str_dict = BotlangSystem.run(
            '(to-json (make-dict (list (cons "a" 1))))'
        )
        self.assertEqual(str_dict, json.dumps({'a': 1}))
