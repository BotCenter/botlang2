import unittest
import time
from botlang.interpreter import BotlangSystem

class TimeTestCase(unittest.TestCase):

    def test_time_now(self):
        time_now_python = time.time()
        time_now_botlang = BotlangSystem.run("""
            (time-now)
        """)
        self.assertAlmostEqual(time_now_python, time_now_botlang, delta=5)

    def test_time_add_seconds(self):
        time_plus = BotlangSystem.run("""
            (define init_time 100)
            (time-delta-seconds init_time 30)
        """)
        self.assertEqual(time_plus, 100 + 30)

        time_less = BotlangSystem.run("""
              (define init_time 100)
              (time-delta-seconds init_time -30)
          """)
        self.assertEqual(time_less, 100 - 30)

        time_now = time.time()
        time_plus30 = time_now + 30
        result = BotlangSystem.run("""
            (define init_time """ + str(time_now) + """ )
            (time-delta-seconds init_time 30)
            """)
        self.assertEqual(time_plus30, result)

    def test_time_add_minutes(self):
        time_plus = BotlangSystem.run("""
            (define init_time 120)
            (time-delta-minutes init_time 30)
        """)
        self.assertEqual(time_plus, 120 + 30*60)

        time_less = BotlangSystem.run("""
            (define init_time 120)
            (time-delta-minutes init_time -30)
        """)
        self.assertEqual(time_less, 120 - 30*60)

        time_now = time.time()
        time_plus30 = time_now + 30 * 60
        result = BotlangSystem.run("""
            (define init_time """ + str(time_now) + """ )
            (time-delta-minutes init_time 30)
            """)
        self.assertEqual(time_plus30, result)

    def test_time_add_hours(self):
        time_plus = BotlangSystem.run("""
            (define init_time 130)
            (time-delta-hours init_time 30)
        """)
        self.assertEqual(time_plus, 130 + 30*60*60)

        time_less = BotlangSystem.run("""
            (define init_time 130)
            (time-delta-hours init_time -30)
        """)
        self.assertEqual(time_less, 130 - 30*60*60)

        time_now = time.time()
        time_plus30 = time_now + 30 * 60 * 60
        result = BotlangSystem.run("""
            (define init_time """ + str(time_now) + """ )
            (time-delta-hours init_time 30)
            """)
        self.assertEqual(time_plus30, result)

    def test_time_add_days(self):
        time_plus = BotlangSystem.run("""
            (define init_time 150)
            (time-delta-days init_time 30)
        """)
        self.assertEqual(time_plus, 150 + 30*60*60*24)

        time_less = BotlangSystem.run("""
            (define init_time 150)
            (time-delta-days init_time -30)
        """)
        self.assertEqual(time_less, 150 - 30*60*60*24)

        time_now = time.time()
        time_plus30 = time_now + 30 * 60 * 60 * 24
        result = BotlangSystem.run("""
            (define init_time """ + str(time_now) + """ )
            (time-delta-days init_time 30)
            """)
        self.assertEqual(time_plus30, result)

    def test_time_string(self):
        time_parsed_seconds = time.mktime(time.strptime("30 Nov 00", "%d %b %y"))
        time_botlang = BotlangSystem.run("""
            (time-string "30 Nov 00" "%d %b %y")
        """)
        self.assertEqual(time_parsed_seconds, time_botlang)


