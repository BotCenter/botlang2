from unittest import TestCase

from botlang import BotlangSystem
from botlang.environment.primitives.oop import CLASS_REFERENCE_KEY
from botlang.evaluation.values import FunVal


class BotlangClassesTestCase(TestCase):

    TEST_CLASS = """
    (defclass Car
        [wheels 4]
        [speed 0]
        [accelerate (fun (self amount)
            (@! self "speed" (+ (@ self "speed") amount))
        )]
    )
    """

    def test_class_definition(self):

        code = '{} Car'.format(self.TEST_CLASS)
        car_class = BotlangSystem.run(code)
        self.assertTrue(isinstance(car_class, dict))

        class_members = car_class['members']
        self.assertEqual(class_members['wheels'], 4)
        self.assertEqual(class_members['speed'], 0)
        self.assertTrue(isinstance(class_members['accelerate'], FunVal))

    def test_class_instance(self):

        code = "{} (new Car)".format(self.TEST_CLASS)
        car_instance = BotlangSystem.run(code)
        self.assertTrue(isinstance(car_instance, dict))
        self.assertEqual(car_instance['wheels'], 4)

        code = """{}
        (define my-car (new Car))
        (@! my-car "speed" 2)
        (cons Car my-car)
        """.format(self.TEST_CLASS)
        car_class, car_instance = BotlangSystem.run(code)
        self.assertEqual(car_class['members']['speed'], 0)
        self.assertEqual(car_instance['speed'], 2)
        self.assertEqual(car_instance[CLASS_REFERENCE_KEY], car_class)

    def test_method_invocation(self):

        code = """{}
        (define my-car (new Car))
        (@@ my-car "accelerate" 2)
        (@ my-car "speed") 
        """.format(self.TEST_CLASS)
        self.assertEqual(BotlangSystem.run(code), 2)
