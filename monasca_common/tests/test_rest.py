# coding=utf-8
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock

from oslotest import base

from monasca_common.rest import exceptions
from monasca_common.rest import utils


class TestRestUtils(base.BaseTestCase):

    def setUp(self):
        super(TestRestUtils, self).setUp()

    def tearDown(self):
        super(TestRestUtils, self).tearDown()

    def test_read_body_with_success(self):
        self.mock_json_patcher = mock.patch('monasca_common.rest.utils.jsonutils')
        self.mock_json = self.mock_json_patcher.start()
        self.mock_json.loads.return_value = ""
        payload = mock.Mock()

        utils.read_body(payload)

        self.mock_json.loads.assert_called_once_with(payload.read.return_value)

    def test_read_body_empty_content_in_payload(self):
        payload = mock.Mock()
        payload.read.return_value = None

        self.assertIsNone(utils.read_body(payload))

    def test_read_body_json_loads_exception(self):
        payload = mock.Mock()

        self.assertRaises(exceptions.DataConversionException,
                          utils.read_body, payload)

    def test_read_body_unsupported_content_type(self):
        unsupported_content_type = mock.Mock()

        self.assertRaises(
            exceptions.UnsupportedContentTypeException, utils.read_body, None,
            unsupported_content_type)

    def test_read_body_unreadable_content_error(self):
        unreadable_content = mock.Mock()
        unreadable_content.read.side_effect = Exception

        self.assertRaises(
            exceptions.UnreadableContentError,
            utils.read_body, unreadable_content)

    def test_as_json(self):
        self.assertEqual(b'{"\xc4\x85": "\xc4\x99"}', utils.as_json({'ą': 'ę'}))

    def test_as_json_ensure_ascii(self):
        self.assertEqual(b'{"\u0105": "\u0119"}', utils.as_json({'ą': 'ę'}, ensure_ascii=True))
