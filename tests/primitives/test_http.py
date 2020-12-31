from unittest import TestCase, mock
from urllib.parse import quote

import responses

from botlang import BotlangSystem


class HttpTestCase(TestCase):

    def test_uri_escape(self):

        test_segment = "Pascual Baburizza 595"
        unescaped = BotlangSystem.run('"%s"' % test_segment)
        escaped = BotlangSystem.run('(uri-escape "%s")' % test_segment)
        expected = quote(test_segment)

        self.assertNotEqual(unescaped, expected)
        self.assertEqual(escaped, expected)

    @responses.activate
    def test_http_responses(self):

        responses.add(
            responses.GET,
            'http://example.com',
            json={'key': 'value'},
            status=200
        )
        response = BotlangSystem.run('(http-get "http://example.com")')
        self.assertEqual(response['status-code'], 200)
        self.assertEqual(
            response['headers']['Content-Type'], 'application/json'
        )
        self.assertDictEqual(response['json'], {'key': 'value'})
        self.assertEqual(response['encoding'], 'utf-8')

        responses.add(
            responses.GET,
            'http://example2.com',
            body='Hola',
            status=206
        )
        response = BotlangSystem.run('(http-get "http://example2.com")')
        self.assertEqual(response['status-code'], 206)
        self.assertEqual(response['headers']['Content-Type'], 'text/plain')
        self.assertEqual(response['text'], 'Hola')

        responses.add(
            responses.GET,
            'http://example3.com',
            body='Not found',
            status=404,
            headers={'X-Hello': 'A value'}
        )
        response = BotlangSystem.run('(http-get "http://example3.com")')
        self.assertEqual(response['status-code'], 404)
        self.assertEqual(response['headers']['X-Hello'], 'A value')
        self.assertEqual(response['text'], 'Not found')

    @mock.patch('requests.post')
    def test_http_post_json_no_headers(self, mock_post):

        payload = '(make-dict (list (cons "key" "value")))'
        BotlangSystem.run('(http-post "http://some.url" %s)' % payload)
        post_call_args = mock_post.call_args[0]
        url = post_call_args[0]

        post_call_kwargs = mock_post.call_args[1]
        headers = post_call_kwargs['headers']
        json = post_call_kwargs['json']

        self.assertEqual(url, 'http://some.url')
        self.assertIsNone(headers)
        self.assertDictEqual(json, {'key': 'value'})

    @mock.patch('requests.post')
    def test_http_post_json_with_headers(self, mock_post):

        payload = '(make-dict (list (cons "key" "value")))'
        headers = '(make-dict (list (cons "a-header" "its-value")))'
        BotlangSystem.run(
            '(http-post "http://some.url" %s %s)' % (payload, headers)
        )
        post_call_args = mock_post.call_args[0]
        url = post_call_args[0]

        post_call_kwargs = mock_post.call_args[1]
        headers = post_call_kwargs['headers']
        json = post_call_kwargs['json']

        self.assertIsNone(post_call_kwargs.get('data'))
        self.assertEqual(url, 'http://some.url')
        self.assertDictEqual(headers, {'a-header': 'its-value'})
        self.assertDictEqual(json, {'key': 'value'})

    @mock.patch('requests.post')
    def test_http_post_form(self, mock_post):

        payload = '(make-dict (list (cons "key" "value")))'
        headers = '(make-dict (list (cons "a-header" "its-value")))'
        BotlangSystem.run(
            '(http-post-form "http://some.url" %s %s)' % (payload, headers)
        )
        post_call_args = mock_post.call_args[0]
        url = post_call_args[0]

        post_call_kwargs = mock_post.call_args[1]
        headers = post_call_kwargs['headers']
        data = post_call_kwargs['data']

        self.assertIsNone(post_call_kwargs.get('json'))
        self.assertEqual(url, 'http://some.url')
        self.assertDictEqual(headers, {'a-header': 'its-value'})
        self.assertDictEqual(data, {'key': 'value'})

    @mock.patch('requests.delete')
    def test_http_delete(self, mock_delete):

        headers = '(make-dict (list (cons "a-header" "its-value")))'
        BotlangSystem.run(
            '(http-delete "http://some.url" %s)' % headers
        )
        call_args = mock_delete.call_args[0]
        url = call_args[0]

        call_kwargs = mock_delete.call_args[1]
        headers = call_kwargs['headers']

        self.assertIsNone(call_kwargs.get('json'))
        self.assertEqual(url, 'http://some.url')
        self.assertDictEqual(headers, {'a-header': 'its-value'})
