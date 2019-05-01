from unittest import TestCase

from botlang import BotlangSystem


class ExceptionsTestCase(TestCase):

    def test_exception_values(self):

        self.assertFalse(BotlangSystem().eval('(exception? #t)'))
        self.assertFalse(BotlangSystem().eval('(exception? nil)'))
        self.assertTrue(BotlangSystem().eval(
            '(exception? (try-catch (fun () (get (make-dict) 1)) (fun (e) e)))'
        ))
        self.assertFalse(BotlangSystem().eval(
            '(exception? (try-catch (fun () (get (list 1) 0)) (fun (e) e)))'
        ))
        self.assertTrue(BotlangSystem().eval(
            '(exception? (try-catch (fun () (get (list 1) 1)) (fun (e) e)))'
        ))

    def test_success(self):

        code = r"""
        (define dict (make-dict (list)))
        (try-catch
            (function () dict)
            (function () (put! dict "msg" "I won't be called"))
        )
        """
        result = BotlangSystem.run(code)
        self.assertEqual(len(result.values()), 0)

    def test_catch(self):

        complex_botlang = r"""
        [defun fatal-error () (/ 1 0)]
        [defun failure (arg) "Hello"]
        (try-catch fatal-error failure)
        """
        try:
            result = BotlangSystem.run(complex_botlang)
            self.assertEqual(result, 'Hello')
        except Exception:
            self.fail("Try-catch failed")

        complex_botlang = r"""
        [define context (make-dict (list))]
        [defun process () (get (make-dict (list)) 1)]
        [defun failure (arg) (put! context "error" arg) ]
        (try-catch-verbose process failure)
        (get context "error")
        """

        result = BotlangSystem.run(complex_botlang)
        self.assertEqual(result.name, 'system')
        self.assertEqual(
            result.description, 'Collection does not have key/index %s' % '1'
        )

        # Python errors
        complex_botlang = r"""
                [define context (make-dict (list))]
                [defun fatal-error () (/ 1 0)]
                [defun failure (arg) (put! context "error" arg) ]
                (try-catch fatal-error failure)
                (get context "error")
                """
        result = BotlangSystem.run(complex_botlang)
        self.assertEqual(result.name, 'system')
        self.assertEqual(result.description, 'system')

        complex_botlang = r"""
                [define context (make-dict (list))]
                [defun fatal-error () (/ 1 0)]
                [defun failure (arg) (put! context "error" arg) ]
                (try-catch-verbose fatal-error failure)
                (get context "error")
                """
        result = BotlangSystem.run(complex_botlang)
        self.assertEqual(result.name, 'system')
        self.assertRegex(result.description, 'division by zero')

        # Catch returns a value
        code = r"""
        (try-catch
            (function () (/ 1 0))
            (function (e) "Hi")
        )
        """
        self.assertEqual(BotlangSystem.run(code), 'Hi')

    def test_finally(self):

        complex_botlang = r"""
        [define context (make-dict (list))]
        [defun fatal-error () (/ 1 0)]
        [defun failure (arg) (put! context "error" arg) ]
        [defun finally () (put! context "success" "Finally called")]
        (try-catch-verbose fatal-error failure finally)
        context
        """
        result = BotlangSystem.run(complex_botlang)
        error = result.get('error')
        finally_result = result.get('success')
        self.assertEqual(error.name, 'system')
        self.assertRegex(error.description, 'division by zero')
        self.assertEqual(finally_result, 'Finally called')

        # Finally value is always the one returned
        code = "(try-catch (fun () 1) (fun (e) 2) (fun () 3))"
        self.assertEqual(BotlangSystem.run(code), 3)

        code = "(try-catch (fun () (/ 1 0)) (fun (e) 2) (fun () 3))"
        self.assertEqual(BotlangSystem.run(code), 3)
