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

import falcon
from oslotest import base

from monasca_common.rest import exceptions
from monasca_common.rest import utils


class TestRestUtils(base.BaseTestCase):

    def setUp(self):
        super(TestRestUtils, self).setUp()
        self.mock_json_patcher = mock.patch('monasca_common.rest.utils.json')
        self.mock_json = self.mock_json_patcher.start()

    def tearDown(self):
        super(TestRestUtils, self).tearDown()
        self.mock_json_patcher.stop()

    def test_read_body_with_success(self):
        self.mock_json.loads.return_value = ""
        payload = mock.Mock()

        utils.read_body(payload)

        self.mock_json.loads.assert_called_once_with(payload.read.return_value)

    def test_read_body_empty_content_in_payload(self):
        self.mock_json.loads.return_value = ""
        payload = mock.Mock()
        payload.read.return_value = None

        self.assertIsNone(utils.read_body(payload))

    def test_read_body_json_loads_exception(self):
        self.mock_json.loads.side_effect = Exception
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

    def test_as_json_success(self):
        data = mock.Mock()

        dumped_json = utils.as_json(data)

        self.assertEqual(dumped_json, self.mock_json.dumps.return_value)

    def test_as_json_with_exception(self):
        data = mock.Mock()
        self.mock_json.dumps.side_effect = Exception

        self.assertRaises(exceptions.DataConversionException,
                          utils.as_json, data)


class TestRoleValidation(base.BaseTestCase):

    def test_role_valid(self):
        req_roles = 'role0', 'rOlE1'
        authorized_roles = ['RolE1', 'Role2']

        req = mock.Mock()
        req.roles = req_roles

        utils.validate_authorization(req, authorized_roles)

    def test_role_invalid(self):
        req_roles = 'role2', 'role3'
        authorized_roles = ['role0', 'role1']

        req = mock.Mock()
        req.roles = req_roles

        self.assertRaises(
            falcon.HTTPUnauthorized,
            utils.validate_authorization, req, authorized_roles)

    def test_empty_role_header(self):
        req_roles = []
        authorized_roles = ['Role1', 'Role2']

        req = mock.Mock()
        req.roles = req_roles

        self.assertRaises(
            falcon.HTTPUnauthorized,
            utils.validate_authorization, req, authorized_roles)

    def test_no_role_header(self):
        req_roles = None
        authorized_roles = ['Role1', 'Role2']

        req = mock.Mock()
        req.roles = req_roles

        self.assertRaises(
            falcon.HTTPUnauthorized,
            utils.validate_authorization, req, authorized_roles)


class TestGetQueryDimension(base.BaseTestCase):

    def test_no_dimensions(self):
        result = utils.get_query_dimensions(None)
        self.assertEqual({}, result)

    def test_one_dimension(self):
        result = utils.get_query_dimensions('Dimension:Value')
        self.assertEqual({"Dimension": "Value"}, result)

    def test_comma_sep_dimensions(self):
        result = utils.get_query_dimensions(
            'Dimension:Value,Dimension-2:Value-2')
        self.assertEqual(
            {"Dimension": "Value", "Dimension-2": "Value-2"}, result)

    def test_many_comma_sep_dimensions(self):
        result = utils.get_query_dimensions(
            'Dimension-3:Value-3,Dimension:Value,Dimension-2:Value-2')
        self.assertEqual(
            {"Dimension": "Value",
             "Dimension-2": "Value-2",
             "Dimension-3": "Value-3"}, result)

    def test_dimension_no_value(self):
        result = utils.get_query_dimensions('Dimension_no_value')
        self.assertEqual({"Dimension_no_value": ""}, result)

    def test_dimension_multi_value(self):
        result = utils.get_query_dimensions('Dimension_multi_value:one|two|three')
        self.assertEqual({"Dimension_multi_value": "one|two|three"}, result)

    def test_dimension_list(self):
        result = utils.get_query_dimensions(
            ['Dimension:Value', 'Dimension-2:Value-2,Dimension-3:Value-3'])
        self.assertEqual(
            {"Dimension": "Value",
             "Dimension-2": "Value-2",
             "Dimension-3": "Value-3"}, result)

    def test_invalid_dimension(self):
        self.assertRaises(exceptions.HTTPUnprocessableEntityError,
                          utils.get_query_dimensions,
                          {'foo'})

    def test_dimension_with_multiple_colons(self):
        result = utils.get_query_dimensions(
            'url:http://192.168.10.4:5601,'
            'hostname:monasca,'
            'component:kibana,'
            'service:monitoring')
        self.assertEqual({"url": "http://192.168.10.4:5601",
                          "hostname": "monasca",
                          "component": "kibana",
                          "service": "monitoring"}, result)


class TestTimestampsValidation(base.BaseTestCase):

    def test_valid_timestamps(self):
        start_time = '2015-01-01T00:00:00Z'
        end_time = '2015-01-01T00:00:01Z'
        start_timestamp = utils._convert_time_string(start_time)
        end_timestamp = utils._convert_time_string(end_time)
        self.assertIsNone(
            utils.validate_timestamp_order(start_timestamp, end_timestamp))

    def test_same_timestamps(self):
        start_time = '2015-01-01T00:00:00Z'
        end_time = start_time
        start_timestamp = utils._convert_time_string(start_time)
        end_timestamp = utils._convert_time_string(end_time)

        self.assertRaises(
            exceptions.HTTPUnprocessableEntityError,
            utils.validate_timestamp_order,
            start_timestamp, end_timestamp)

    def test_end_before_than_start(self):
        start_time = '2015-01-01T00:00:00Z'
        end_time = '2014-12-31T23:59:59Z'
        start_timestamp = utils._convert_time_string(start_time)
        end_timestamp = utils._convert_time_string(end_time)

        self.assertRaises(
            exceptions.HTTPUnprocessableEntityError,
            utils.validate_timestamp_order,
            start_timestamp, end_timestamp)

    def test_until_end(self):
        end_time = '2014-12-31T23:59:59Z'
        end_timestamp = utils._convert_time_string(end_time)
        self.assertIsNone(
            utils.validate_timestamp_order(None, end_timestamp))

    def test_from_start(self):
        start_time = '2014-12-31T23:59:59Z'
        start_timestamp = utils._convert_time_string(start_time)
        self.assertIsNone(
            utils.validate_timestamp_order(start_timestamp, None))

    def test_all_time(self):
        self.assertIsNone(
            utils.validate_timestamp_order(None, None))


class TestGetQueryTimestamp(base.BaseTestCase):

    def test_valid_date_time_string(self):
        date_time_string = '2015-01-01T00:00:00Z'

        timestamp = utils.get_query_timestamp(date_time_string)
        self.assertEqual(1420070400., timestamp)

    def test_valid_date_time_string_with_mills(self):
        date_time_string = '2015-01-01T00:00:00.025Z'

        timestamp = utils.get_query_timestamp(date_time_string)
        self.assertEqual(1420070400.025, timestamp)

    def test_valid_date_time_string_with_timezone(self):
        date_time_string = '2015-01-01T09:00:00+09:00'

        timestamp = utils.get_query_timestamp(date_time_string)
        self.assertEqual(1420070400., timestamp)

    def test_invalid_date_time_string(self):
        date_time_string = '2015-01-01T00:00:000Z'

        self.assertRaises(
            exceptions.HTTPUnprocessableEntityError,
            utils.get_query_timestamp, date_time_string)


class TestValidateQueryDimensions(base.BaseTestCase):

    def test_validate_query_dimension(self):
        dimensions = {'foo': 'bar'}
        actual = utils.validate_query_dimensions(dimensions)
        expected = {'foo': ['bar']}
        self.assertDictEqual(actual, expected)

    def test_validate_query_no_value(self):
        dimensions = {'foo': None}
        actual = utils.validate_query_dimensions(dimensions)
        expected = {'foo': None}
        self.assertDictEqual(actual, expected)

    def test_validate_query_dimension_multiple_keys(self):
        dimensions = {'foo': 'a|b|c'}
        actual = utils.validate_query_dimensions(dimensions)
        expected = {'foo': ['a', 'b', 'c']}
        self.assertDictEqual(actual, expected)

    def test_validate_invalid_key(self):
        dimensions = {'foo': None, '_invalid': 'bar'}
        self.assertRaises(
            exceptions.HTTPUnprocessableEntityError,
            utils.validate_query_dimensions,
            dimensions)
