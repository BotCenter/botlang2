from unittest import TestCase

from botlang import BotlangSystem
from botlang.evaluation.oop import OopHelper
from botlang.evaluation.values import FunVal


class BotlangClassesTestCase(TestCase):

    TEST_CLASS = """
    (defclass Car
        [attributes
            (wheels 4)
            (speed 0)
        ]
        [methods
            [accelerate (fun (self amount)
                (@! self "speed" (+ (@ self "speed") amount))
            )]
        ]
    )
    """

    TEST_HIERARCHY = """
    (defclass Vehicle
        [attributes
            (speed 0)
            wheels
        ]
        [methods
            [accelerate (fun (self amount)
                (@! self "speed" (+ (@ self "speed") amount))
            )]
        ]
    )
    (defclass Car
        [extends Vehicle]
        [attributes (wheels 4) (lights-state "OFF")]
        [methods
            [turn-lights-on  (fun (self) (@! self "lights-state" "ON"))]
            [turn-lights-off (fun (self) (@! self "lights-state" "OFF"))]
        ]
    )
    (defclass Plane
        [extends Vehicle]
        [attributes (wheels 10) (wings 2)]
        [methods
            [accelerate (fun (self amount)
                (define speed (+ (@ self "speed") (* 5 amount)))
                (@! self "speed" speed) ; planes are very fast!
            )]
        ]
    )
    """

    def test_class_definition(self):

        code = '{} Car'.format(self.TEST_CLASS)
        car_class = BotlangSystem.run(code)
        self.assertTrue(isinstance(car_class, dict))

        # Superclass is Object
        self.assertEqual(
            car_class[OopHelper.SUPERCLASS_KEY][OopHelper.CLASS_NAME_KEY],
            OopHelper.BASE_CLASS_NAME
        )

        attributes = car_class[OopHelper.INSTANCE_ATTRS_KEY]
        self.assertEqual(attributes['wheels'], 4)
        self.assertEqual(attributes['speed'], 0)

        methods = car_class[OopHelper.METHODS_KEY]
        self.assertTrue(isinstance(methods['accelerate'], FunVal))

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
        self.assertEqual(car_class[OopHelper.INSTANCE_ATTRS_KEY]['speed'], 0)
        self.assertEqual(car_instance['speed'], 2)
        self.assertEqual(car_instance[OopHelper.CLASS_REFERENCE_KEY], car_class)

    def test_method_invocation(self):

        code = """{}
        (define my-car (new Car))
        (send my-car "accelerate" 2)
        (@ my-car "speed") 
        """.format(self.TEST_CLASS)
        self.assertEqual(BotlangSystem.run(code), 2)

    def test_inheritance(self):

        code = '{} (new Car)'.format(self.TEST_HIERARCHY)
        car_instance = BotlangSystem.run(code)
        self.assertEqual(car_instance['lights-state'], 'OFF')
        self.assertEqual(car_instance['speed'], 0)
        self.assertEqual(car_instance['wheels'], 4)

        code = """{}
        (define my-car (new Car))
        (send my-car "turn-lights-on")
        (send my-car "accelerate" 5)
        my-car
        """.format(self.TEST_HIERARCHY)

        car_instance = BotlangSystem.run(code)
        self.assertEqual(car_instance['lights-state'], 'ON')
        self.assertEqual(car_instance['speed'], 5)

    def test_subtype_polymorphism(self):

        code = """{}
        (define vehicles (list (new Car) (new Plane)))
        (map
            (fun (vehicle) (send vehicle "accelerate" 3))
            vehicles
        )
        """.format(self.TEST_HIERARCHY)

        car, plane = BotlangSystem.run(code)
        self.assertEqual(car['speed'], 3)
        self.assertEqual(plane['speed'], 15)
