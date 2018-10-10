from unittest import TestCase

from botlang import BotlangSystem
from botlang.evaluation.oop import OopHelper, CLASS_REFERENCE_KEY, \
    INSTANCE_ATTRS_KEY, CLASS_NAME_KEY, SUPERCLASS_KEY, METHODS_KEY
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

    TEST_HIERARCHY_2 = """
    (defclass Product
        [attributes id category name price]
        [methods
            (init (fun (self id category name price)
                (@! self "id" id)
                (@! self "category" category)
                (@! self "name" name)
                (@! self "price" price)
            ))
        ]
    )
    
    (defclass ShoppingCart
        [attributes
            (products (make-dict))
        ]
        [methods
            (add-product (fun (self product)
                (put! (@ self "products") (@ product "id") product)
            ))
            (get-products (fun (self)
                (map
                    (fun (product) (send product "serialize"))
                    (values (@ self "products"))
                )
            ))
        ]
    )
    """

    TEST_DEEP_HIERARCHY = """
    (defclass Product
        [attributes id category name price]
        [methods
            (init (fun (self id category name price)
                (@! self "id" id)
                (@! self "category" category)
                (@! self "name" name)
                (@! self "price" price)
            ))
        ]
    )
    
    (defclass Cheese
        [extends Product]
        [methods
            (init (fun (self id name price)
                (super self "init" id "Cheese" name price)
            ))
        ]
    )
    
    (defclass Camembert
        [extends Cheese]
        [methods
            (init (fun (self id price)
                (super self "init" id "Camembert" price)
            ))
        ]
    )
    
    (defclass CheapCamembert
        [extends Camembert]
        [methods
            (init (fun (self id)
                (super self "init" id 2000)
            ))
        ]
    )
    """

    def test_class_definition(self):

        code = '{} Car'.format(self.TEST_CLASS)
        car_class = BotlangSystem.run(code)
        self.assertTrue(isinstance(car_class, dict))

        # Superclass is Object
        self.assertEqual(
            car_class[SUPERCLASS_KEY][CLASS_NAME_KEY],
            OopHelper.OBJECT_CLASS_NAME
        )

        attributes = car_class[INSTANCE_ATTRS_KEY]
        self.assertEqual(attributes['wheels'], 4)
        self.assertEqual(attributes['speed'], 0)

        methods = car_class[METHODS_KEY]
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
        self.assertEqual(car_class[INSTANCE_ATTRS_KEY]['speed'], 0)
        self.assertEqual(car_instance['speed'], 2)
        self.assertEqual(car_instance[CLASS_REFERENCE_KEY], car_class)

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

    def test_default_serialize_method(self):

        code = """{}
        (define car (new Car))
        (cons car (send car "serialize"))
        """.format(self.TEST_CLASS)

        car, serialized_car = BotlangSystem.run(code)
        self.assertEqual(len(car.items()), len(serialized_car.items()))
        self.assertEqual(
            serialized_car[CLASS_REFERENCE_KEY],
            car[CLASS_REFERENCE_KEY][CLASS_NAME_KEY]
        )
        self.assertEqual(car['speed'], serialized_car['speed'])
        self.assertEqual(car['wheels'], serialized_car['wheels'])

    def test_attributes(self):

        code = """{}
        (define cart (new ShoppingCart))
        (map
            (fun (product) (send cart "add-product" product))
            (list
                (new Product "id1" "food" "Producto 1" 1000)
                (new Product "id2" "food" "Producto 2" 3000)
                (new Product "id3" "food" "Producto 3" 2000)
            )
        )
        (send cart "get-products")
        """.format(self.TEST_HIERARCHY_2)

        p1, p2, p3 = BotlangSystem.run(code)
        self.assertEqual(len(p1.keys()), 5)
        self.assertEqual(p1['id'], 'id1')
        self.assertEqual(p1['category'], 'food')
        self.assertEqual(p1['name'], 'Producto 1')
        self.assertEqual(p1['price'], 1000)
        self.assertEqual(p1[CLASS_REFERENCE_KEY], 'Product')

    def test_super(self):

        code = """{}
        (defclass Wine
            (extends Product)
            (methods
                (init (fun (self id name price)
                    (super self "init" id "wine" name price)
                ))
            )
        )
        (send (new Wine "gato1" "Gato" 2000) "serialize")
        """.format(self.TEST_HIERARCHY_2)

        wine = BotlangSystem.run(code)
        self.assertEqual(len(wine.keys()), 5)
        self.assertEqual(wine['id'], 'gato1')
        self.assertEqual(wine['category'], 'wine')
        self.assertEqual(wine['name'], 'Gato')
        self.assertEqual(wine['price'], 2000)
        self.assertEqual(wine[CLASS_REFERENCE_KEY], 'Wine')

        code = """{}
        (send (new CheapCamembert "id1") "serialize")
        """.format(self.TEST_DEEP_HIERARCHY)

        camembert = BotlangSystem.run(code)
        self.assertEqual(len(camembert.keys()), 5)
        self.assertEqual(camembert['id'], 'id1')
        self.assertEqual(camembert['category'], 'Cheese')
        self.assertEqual(camembert['name'], 'Camembert')
        self.assertEqual(camembert['price'], 2000)
        print(camembert)
        self.assertEqual(camembert[CLASS_REFERENCE_KEY], 'CheapCamembert')

    def test_class_side(self):

        code = """
        (defclass Singleton
            [attributes (data 10)]
            [class-attributes instance]
            [class-methods
                (get-instance (fun (cls)
                    (define instance (@ cls "instance"))
                    (if (nil? instance)
                        (begin
                            (define new-instance (new cls))
                            (@! cls "instance" new-instance)
                            new-instance
                        )
                        instance
                    )
                ))
            ]
        )
        (list
            (send Singleton "get-instance")
            (send Singleton "get-instance")
            (send Singleton "get-instance")
        )
        """
        i1, i2, i3 = BotlangSystem.run(code)
        self.assertTrue(i1 is i2)
        self.assertTrue(i2 is i3)
