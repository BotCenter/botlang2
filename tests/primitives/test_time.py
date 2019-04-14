import calendar
import unittest
import time

from datetime import datetime

import pytz

from botlang.environment.primitives.datetime import time_localize, \
    time_from_string
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

    def test_time_from_string(self):
        time_parsed_seconds = calendar.timegm(
            time.strptime("30 Nov 00", "%d %b %y")
        )
        time_botlang = BotlangSystem.run('(time-from-string "30 Nov 00")')
        self.assertEqual(time_parsed_seconds, time_botlang)

    def test_time_to_string(self):
        time = 975553200  # 30 nov 00
        result = BotlangSystem.run("""
            (time-to-string """ + str(time) + """ "%d %b %y")
        """)
        self.assertEqual("30 Nov 00", result)

    def test_time_localize(self):
        t = time_from_string('14 Apr 19 18:00')
        self.assertEqual(datetime.fromtimestamp(t, tz=pytz.utc).hour, 18)

        locale = 'America/Santiago'  # UTC-4
        localized = time_localize(t, locale)
        self.assertEqual(localized.hour, 14)

    def test_time_weekday(self):
        t = '(time-from-string "14 Apr 19")'
        weekday = BotlangSystem.run('(time-weekday %s)' % t)
        self.assertEqual(weekday, 6)

        weekday_iso = BotlangSystem.run('(time-weekday-iso %s)' % t)
        self.assertEqual(weekday_iso, 7)

        weekday_es = BotlangSystem.run('(time-weekday-str %s "ES")' % t)
        self.assertEqual(weekday_es, 'domingo')

        weekday_es = BotlangSystem.run('(time-weekday-str %s "EN")' % t)
        self.assertEqual(weekday_es, 'sunday')

    def test_time_part_extractors(self):
        t = '(time-from-string "14 Apr 19 18:30:12")'
        weekday = BotlangSystem.run('(time-year %s)' % t)
        self.assertEqual(weekday, 2019)

        weekday = BotlangSystem.run('(time-month %s)' % t)
        self.assertEqual(weekday, 4)

        weekday = BotlangSystem.run('(time-day %s)' % t)
        self.assertEqual(weekday, 14)

        weekday = BotlangSystem.run('(time-hour %s)' % t)
        self.assertEqual(weekday, 18)

        weekday = BotlangSystem.run('(time-hour %s "America/Santiago")' % t)
        self.assertEqual(weekday, 14)

        weekday = BotlangSystem.run('(time-minute %s)' % t)
        self.assertEqual(weekday, 30)

        weekday = BotlangSystem.run('(time-second %s)' % t)
        self.assertEqual(weekday, 12)
