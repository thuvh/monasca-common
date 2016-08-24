# (C) Copyright 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import monasca_common.validation.metrics as metric_validator
import unittest

# a few valid characters to test
valid_name_chars = ".'_-"
invalid_name_chars = " <>={}(),\"\\\\;&"

# a few valid characters to test
valid_dimension_chars = " .'_-"
invalid_dimension_chars = "<>={}(),\"\\\\;&"


class TestMetricValidation(unittest.TestCase):
    def test_valid_single_metric(self):
        metric = {"name": "test_metric_name",
                  "dimensions": {"key1": "value1",
                                 "key2": "value2"},
                  "timestamp": 1405630174123,
                  "value": 5}
        metric_validator.validate(metric)

    def test_valid_metrics(self):
        metrics = [
            {"name": "name1",
             "dimensions": {"key1": "value1",
                            "key2": "value2"},
             "timestamp": 1405630174123,
             "value": 1.0},
            {"name": "name2",
             "dimensions": {"key1": "value1",
                            "key2": "value2"},
             "value_meta": {"key1": "value1",
                            "key2": "value2"},
             "timestamp": 1405630174123,
             "value": 2.0}
        ]
        metric_validator.validate(metrics)

    def test_valid_metric_unicode_dimension_value(self):
        metric = {"name": "test_metric_name",
                  "timestamp": 1405630174123,
                  "dimensions": {unichr(2440): 'B', 'B': 'C', 'D': 'E'},
                  "value": 5}
        metric_validator.validate(metric)

    def test_valid_metric_unicode_dimension_key(self):
        metric = {"name": 'test_metric_name',
                  "dimensions": {'A': 'B', 'B': unichr(920), 'D': 'E'},
                  "timestamp": 1405630174123,
                  "value": 5}
        metric_validator.validate(metric)

    def test_valid_metric_unicode_metric_name(self):
        metric = {"name": unichr(6021),
                  "dimensions": {"key1": "value1",
                                 "key2": "value2"},
                  "timestamp": 1405630174123,
                  "value": 5}
        metric_validator.validate(metric)

    def test_invalid_metric_name(self):
        metric = {'name': "TooLarge" * 255,
                  "dimensions": {"key1": "value1",
                                 "key2": "value2"},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidMetricName,
                          metric_validator.validate, metric)

    def test_invalid_metric_name_empty(self):
        metric = {"name": "",
                  "dimensions": {"key1": "value1",
                                 "key2": "value2"},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidMetricName,
                          metric_validator.validate, metric)

    def test_invalid_metric_name_non_str(self):
        metric = {"name": 133,
                  "dimensions": {"key1": "value1",
                                 "key2": "value2"},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidMetricName,
                          metric_validator.validate, metric)

    def test_invalid_metric_restricted_characters(self):
        metric = {"name": '"Foo"',
                  "dimensions": {"key1": "value1",
                                 "key2": "value2"},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidMetricName,
                          metric_validator.validate, metric)

    def test_invalid_dimension_empty_key(self):
        metric = {"name": "test_metric_name",
                  "dimensions": {'A': 'B', '': 'C', 'D': 'E'},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidDimensionKey,
                          metric_validator.validate, metric)

    def test_invalid_dimension_empty_value(self):
        metric = {"name": "test_metric_name",
                  "dimensions": {'A': 'B', 'B': 'C', 'D': ''},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidDimensionValue,
                          metric_validator.validate, metric)

    def test_invalid_dimension_non_str_key(self):
        metric = {"name": "test_metric_name",
                  "dimensions": {'A': 'B', 4: 'C', 'D': 'E'},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidDimensionKey,
                          metric_validator.validate, metric)

    def test_invalid_dimension_non_str_value(self):
        metric = {"name": "test_metric_name",
                  "dimensions": {'A': 13.3, 'B': 'C', 'D': 'E'},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidDimensionValue,
                          metric_validator.validate, metric)

    def test_invalid_dimension_key_length(self):
        metric = {"name": "test_metric_name",
                  "dimensions": {'A'*256: 'B', 'B': 'C', 'D': 'E'},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidDimensionKey,
                          metric_validator.validate, metric)

    def test_invalid_dimension_value_length(self):
        metric = {"name": "test_metric_name",
                  "dimensions": {'A': 'B', 'B': 'C'*256, 'D': 'E'},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidDimensionValue,
                          metric_validator.validate, metric)

    def test_invalid_dimension_key_restricted_characters(self):
        metric = {"name": "test_metric_name",
                  "dimensions": {'A': 'B', 'B': 'C', '(D)': 'E'},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidDimensionKey,
                          metric_validator.validate, metric)

    def test_invalid_dimension_value_restricted_characters(self):
        metric = {"name": "test_metric_name",
                  "dimensions": {'A': 'B;', 'B': 'C', 'D': 'E'},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidDimensionValue,
                          metric_validator.validate, metric)

    def test_invalid_dimension_key_leading_underscore(self):
        metric = {"name": "test_metric_name",
                  "dimensions": {'_A': 'B', 'B': 'C', 'D': 'E'},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidDimensionKey,
                          metric_validator.validate, metric)

    def test_invalid_value(self):
        metric = {"name": "test_metric_name",
                  "dimensions": {"key1": "value1",
                                 "key2": "value2"},
                  "timestamp": 1405630174123,
                  "value": "value"}
        self.assertRaises(metric_validator.InvalidValue,
                          metric_validator.validate, metric)

    def test_valid_name_chars(self):
        for c in valid_name_chars:
            metric = {"name": 'test{}counter'.format(c),
                      "dimensions": {"key1": "value1",
                                     "key2": "value2"},
                      "timestamp": 1405630174123,
                      "value": 5}
            metric_validator.validate(metric)

    def test_invalid_name_chars(self):
        for c in invalid_name_chars:
            metric = {"name": 'test{}counter'.format(c),
                      "dimensions": {"key1": "value1",
                                     "key2": "value2"},
                      "timestamp": 1405630174123,
                      "value": 5}
            self.assertRaises(metric_validator.InvalidMetricName,
                              metric_validator.validate, metric)

    def test_valid_dimension_chars(self):
        for c in valid_dimension_chars:
            metric = {"name": "test_name",
                      "dimensions":
                          {"test{}key".format(c): "test{}value".format(c)},
                      "timestamp": 1405630174123,
                      "value": 5}
            metric_validator.validate(metric)

    def test_invalid_dimension_key_chars(self):
        for c in invalid_dimension_chars:
            metric = {"name": "test_name",
                      "dimensions": {'test{}key'.format(c): 'test-value'},
                      "timestamp": 1405630174123,
                      "value": 5}
            self.assertRaises(metric_validator.InvalidDimensionKey,
                              metric_validator.validate, metric)

    def test_invalid_dimension_value_chars(self):
        for c in invalid_dimension_chars:
            metric = {"name": "test_name",
                      "dimensions":  {'test-key': 'test{}value'.format(c)},
                      "timestamp": 1405630174123,
                      "value": 5}
            self.assertRaises(metric_validator.InvalidDimensionValue,
                              metric_validator.validate, metric)

    def test_invalid_too_many_value_meta(self):
        value_meta = {}
        for i in range(0, 17):
            value_meta['key{}'.format(i)] = 'value{}'.format(i)
        metric = {"name": "test_metric_name",
                  "dimensions": {"key1": "value1",
                                 "key2": "value2"},
                  "value_meta": value_meta,
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidValueMeta,
                          metric_validator.validate, metric)

    def test_invalid_empty_value_meta_key(self):
        metric = {"name": "test_metric_name",
                  "dimensions": {"key1": "value1",
                                 "key2": "value2"},
                  "value_meta": {'': 'BBB'},
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidValueMeta,
                          metric_validator.validate, metric)

    def test_invalid_too_long_value_meta_key(self):
        key = "K"
        for i in range(0, metric_validator.VALUE_META_NAME_MAX_LENGTH):
            key = "{}{}".format(key, "1")
        value_meta = {key: 'BBB'}
        metric = {"name": "test_metric_name",
                  "dimensions": {"key1": "value1",
                                 "key2": "value2"},
                  "value_meta": value_meta,
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidValueMeta,
                          metric_validator.validate, metric)

    def test_invalid_too_large_value_meta(self):
        value_meta_value = ""
        num_value_meta = 10
        for i in range(0, metric_validator.VALUE_META_VALUE_MAX_LENGTH/num_value_meta):
            value_meta_value = '{}{}'.format(value_meta_value, '1')
        value_meta = {}
        for i in range(0, num_value_meta):
            value_meta['key{}'.format(i)] = value_meta_value
        metric = {"name": "test_metric_name",
                  "dimensions": {"key1": "value1",
                                 "key2": "value2"},
                  "value_meta": value_meta,
                  "timestamp": 1405630174123,
                  "value": 5}
        self.assertRaises(metric_validator.InvalidValueMeta,
                          metric_validator.validate, metric)

    def test_invalid_timestamp(self):
        metric = {'name': 'test_metric_name',
                  "dimensions": {"key1": "value1",
                                 "key2": "value2"},
                  "timestamp": "invalid_timestamp",
                  "value": 5}
        self.assertRaises(metric_validator.InvalidTimeStamp,
                          metric_validator.validate, metric)
