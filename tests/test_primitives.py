import unittest

import math

from botlang.interpreter import BotlangSystem


class BotlangTestCase(unittest.TestCase):

    def test_filter(self):

        filtered_list = BotlangSystem.run("""
            (filter (function (v) (> v 3)) (list 5 2 8 9 1 33 -1 -5 4))
        """)
        self.assertEqual(filtered_list, [5, 8, 9, 33, 4])

    def test_sort(self):

        sorted_lists = BotlangSystem.run("""
            [define num-list (list 5 3 0 4 9 1)]
            [define asc-nums (sort (function (a b) (< a b)) num-list)]
            [define desc-nums (sort (function (a b) (> a b)) num-list)]

            [define objs-list
                (list
                    (list "holi" 1)
                    (list "shao" 4)
                    (list "bla" -3)
                    (list "lala" -8)
                )
            ]
            [define asc-objs
                (sort [function (a b) (< (get a 1) (get b 1))] objs-list)
            ]
            [define desc-objs
                (sort [function (a b) (> (get a 1) (get b 1))] objs-list)
            ]

            (make-dict
                (list
                    (list "asc-nums" asc-nums)
                    (list "desc-nums" desc-nums)
                    (list "asc-objs" asc-objs)
                    (list "desc-objs" desc-objs)
                )
            )
        """)
        self.assertEqual(sorted_lists['asc-nums'], [0, 1, 3, 4, 5, 9])
        self.assertEqual(sorted_lists['desc-nums'], [9, 5, 4, 3, 1, 0])
        self.assertEqual(
            sorted_lists['asc-objs'],
            [["lala", -8], ["bla", -3], ["holi", 1], ["shao", 4]]
        )
        self.assertEqual(
            sorted_lists['desc-objs'],
            [["shao", 4], ["holi", 1], ["bla", -3], ["lala", -8]]
        )

    def test_type_conversion(self):

        str_to_num = BotlangSystem.run('(num "666")')
        self.assertEqual(str_to_num, 666)

        num_to_str = BotlangSystem.run('(str 666)')
        self.assertEqual(num_to_str, "666")

    def test_base64(self):

        encoded = BotlangSystem.run('(b64-encode "hólá")')
        self.assertEqual(encoded, 'aMOzbMOh')

        decoded = BotlangSystem.run('(b64-decode "aMOzbMOh")')
        self.assertEqual(decoded, 'hólá')

    def test_string_operations(self):

        lower = BotlangSystem.run('(lowercase "AbCdEfgH")')
        self.assertEqual(lower, "abcdefgh")

        upper = BotlangSystem.run('(uppercase "AbCdEfgH")')
        self.assertEqual(upper, "ABCDEFGH")

        capitalized = BotlangSystem.run('(capitalize "aleluya hmno")')
        self.assertEqual(capitalized, "Aleluya hmno")

        split = BotlangSystem.run('(split "perro,gato,zapallo" ",")')
        self.assertEqual(split, ['perro', 'gato', 'zapallo'])

        join = BotlangSystem.run(
            '(join ", " (list "pollos" "pavos" "iguana"))'
        )
        self.assertEqual(join, 'pollos, pavos, iguana')

        plain = BotlangSystem.run('(plain "ÉnTérO BellákO")')
        self.assertEqual(plain, 'entero bellako')

        replaced = BotlangSystem.run('(replace "muajaja" "j" "h")')
        self.assertEqual(replaced, 'muahaha')

        trimmed = BotlangSystem.run('(trim "   hola, soy julito  ")')
        self.assertEqual(trimmed, 'hola, soy julito')

    def test_compression(self):

        text = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
        velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
        occaecat cupidatat non proident, sunt in culpa qui officia deserunt
        mollit anim id est laborum.
        """

        self.assertEqual(len(text), 511)
        compressed = BotlangSystem.run('(bz2-compress "{0}")'.format(text))
        self.assertEqual(len(compressed), 420)

        decompressed = BotlangSystem.run(
            '(bz2-decompress "{0}")'.format(compressed)
        )
        self.assertEqual(len(decompressed), len(text))

    def test_reverse(self):

        result = BotlangSystem.run('(reverse (list 1 2 3 4))')
        self.assertEqual(result, [4, 3, 2, 1])

        result = BotlangSystem.run('(reverse "sergio")')
        self.assertEqual(result, "oigres")

    def test_enumerate(self):

        result = BotlangSystem.run('(enumerate "abcd")')
        self.assertEqual(result, [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd')])

    def test_sum(self):

        result = BotlangSystem.run('(sum (list 1 2 3 4 10))')
        self.assertEqual(result, 20)

    def test_type(self):

        self.assertTrue(
            BotlangSystem.run('(list? (list 1 2 3))')
        )
        self.assertFalse(
            BotlangSystem.run('(list? "bla")')
        )

    def test_string_append(self):

        self.assertEqual(
            BotlangSystem.run('(append "holi" "hola")'),
            'holihola'
        )

    def test_list_append(self):

        self.assertEqual(
            BotlangSystem.run('(append (list 1 2) (list 3))'),
            [1, 2, 3]
        )

    def test_any_satisfy(self):

        self.assertTrue(
            BotlangSystem.run(
                '(any-satisfy? (fun (x) (equal? x 3)) (list 1 2 3 4))'
            )
        )
        self.assertTrue(
            BotlangSystem.run(
                '(any-satisfy? (fun (x) (equal? x 2)) (list 1 2 3 4))'
            )
        )
        self.assertFalse(
            BotlangSystem.run(
                '(any-satisfy? (fun (x) (equal? x -1)) (list 1 2 3 4))'
            )
        )

    def test_matches(self):

        self.assertTrue(
            BotlangSystem.run(
                '(match? ".*pedro.*" "hola pedro, como estas?")'
            )
        )
        self.assertFalse(
            BotlangSystem.run(
                '(match? ".*pedro.*" "hola julito, como estas?")'
            )
        )

    def test_timestamp(self):

        t0 = math.floor(BotlangSystem.run('(timestamp)'))
        import time
        time.sleep(0.5)
        t1 = round(BotlangSystem.run('(timestamp)'))
        self.assertEqual(t1 - t0, 1)
