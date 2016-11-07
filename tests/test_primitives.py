import unittest
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
