from functools import reduce

from coverage.backunittest import TestCase

from botlang import BotlangSystem
from botlang.environment.primitives.strings.string_functions import string_similarity, \
    remove_same_words
from botlang.evaluation.values import Nil
from botlang.environment.primitives.strings.string_functions import divide_text


class StringPrimitivesTestCase(TestCase):
    list_of_strings = [
        'Servicios Residenciales',
        'Servicios Móviles',
        'Interesado En Contratar O Renovar',
        'Otro'
    ]

    test_strings2 = [
        'Teléfonos móviles',
        'Teléfonos fijos',
        'Computadores'
    ]

    def test_string_similarity(self):
        self.assertEqual(string_similarity('hola', 'hola'), 1)
        self.assertEqual(string_similarity('hola', 'HoLá'), 1)
        self.assertGreater(
            string_similarity('hola', 'holi'),
            string_similarity('hola', 'chao')
        )

        self.assertEqual(string_similarity('', ''), 1)
        self.assertEqual(string_similarity('', 'foo'), 0)
        self.assertEqual(string_similarity('foo', ''), 0)

    def test_remove_same_words(self):
        list_without_duplicates, _ = remove_same_words(self.list_of_strings)
        self.assertSequenceEqual(
            [
                'Residenciales',
                'Móviles',
                'Interesado En Contratar O Renovar',
                'Otro'
            ],
            list_without_duplicates
        )

    @classmethod
    def get_similar_string(cls, test, strings_list):
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

        self.assertEqual(
            self.get_similar_string(
                'otrop', self.list_of_strings
            ),
            self.list_of_strings[3]
        )

        self.assertEqual(
            self.get_similar_string(
                'de otro', self.list_of_strings
            ),
            self.list_of_strings[3]
        )

        self.assertEqual(
            self.get_similar_string(
                'computador', self.test_strings2
            ),
            self.test_strings2[2]
        )
        self.assertEqual(
            self.get_similar_string(
                'telefono movil', self.test_strings2
            ),
            self.test_strings2[0]
        )
        self.assertEqual(
            self.get_similar_string(
                'fijo', self.test_strings2
            ),
            self.test_strings2[1]
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
        self.assertEqual(
            'juan',
            BotlangSystem.run('(match "hola\\s(\\w+).*" "hola juan!!" 1)')
        )

    def test_divide_text(self):
        medium_text = """
        Para reembolsar gastos que no fueron bonificados en línea debe enviarlos a la compañía con el siguiente procedimiento:

        1.       Obtener el aporte correspondiente a la Isapre, Fonasa o cualquier otro beneficio de salud que tenga.
        """

        long_text = """
        Para reembolsar gastos que no fueron bonificados en línea debe enviarlos a la compañía con el siguiente procedimiento:

        1.       Obtener el aporte correspondiente a la Isapre, Fonasa o cualquier otro beneficio de salud que tenga.

        2.       Después de la emisión de los documentos contables por parte de Fonasa/Isapre, existe un plazo de 60 días, dependiendo del convenio, para enviar la solicitud con la siguiente información: a) Formulario Solicitud de Reembolso Gastos Médicos. b) Documentos Originales: Facturas o boletas, Copias del Afiliado de bonos, Órdenes de atención / recetas, Programas médicos, el detalle de prestaciones, en caso de hospitalización u otros. 
         i.      **En el caso de prestaciones no cubiertas por Isapre debe adjuntar boleta original con timbre “sin bonificación” y en caso de Fonasa, indicar que pertenece a Fonasa. 

        3.       Esta información debe ser enviada a la compañía por intermedio de Recursos Humanos, Servicio a Personas de su empleador o ejecutiva que visite su empresa.
        """

        split_text = divide_text(500, medium_text)
        self.assertEqual(len(split_text), 1)

        split_text = divide_text(500, long_text)
        self.assertEqual(len(split_text), 5)
        self.assertEqual(
            split_text[3],
            'i.      **En el caso de prestaciones no cubiertas por Isapre debe'
            ' adjuntar boleta original con timbre “sin bonificación” y en caso'
            ' de Fonasa, indicar que pertenece a Fonasa.'
        )

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
