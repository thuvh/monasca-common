# (C) Copyright 2017 Hewlett Packard Enterprise Development LP
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

from oslotest import base
import pyparsing

from monasca_common.monasca_query_language import aql_parser
from monasca_common.monasca_query_language import query_structures


class TestKafkaProducer(base.BaseTestCase):

    def test_parse_group_expression(self):
        expressions = [
            "",
            "excluding metric_two",
            "group by hostname, service",
            "excluding metric_two group by hostname, service",
            "group by __severity__",
            "excluding {__severity__=HIGH} group by __severity__",
            "excluding {__severity__=HIGH, hostname=host1} group by __severity__, hostname",
            "group by excluding"
        ]
        negative_expressions = [
            "group by hostname excluding {__metricName__=metric_two}",
            "excluding metric_one excluding metric_two",
            "targets metric_one",
        ]
        matchers = [
            [],
            [],
            ["hostname", "service"],
            ["hostname", "service"],
            ["__severity__"],
            ["__severity__"],
            ["__severity__", "hostname"],
            ["excluding"]
        ]
        exclusions = [
            {},
            {"__metricName__": "metric_two"},
            {},
            {"__metricName__": "metric_two"},
            {},
            {"__severity__": "HIGH"},
            {"__severity__": "HIGH", "hostname": "host1"},
            {},
        ]
        for i in range(len(expressions)):
            test_matchers, test_exclusions = aql_parser.parse_group_expression(expressions[i])
            self.assertEqual(test_matchers, matchers[i])
            self.assertEqual(test_exclusions, exclusions[i])
        for i in range(len(negative_expressions)):
            self.assertRaises(query_structures.QueryException,
                              aql_parser.parse_group_expression,
                              negative_expressions[i])

    def test_parse_inhibit_rule(self):
        expressions = [
            "",
            "source metric_one",
            "targets metric_two",
            "source metric_one targets metric_two",
            "source metric_one targets metric_two excluding metric_three",
            "source metric_one targets metric_two excluding metric_three group by hostname",
            "source metric_one targets metric_two group by hostname",
            "source metric_one group by hostname",
            "source {__severity__=HIGH} targets {__severity__=LOW} excluding "
                "{__alarmName__=alarm_one} group by __alarmName__"
        ]
        negative_expressions = [
            "targets metric_two source_metric_one"
        ]
        source = [
            {},
            {"__metricName__": "metric_one"},
            {},
            {"__metricName__": "metric_one"},
            {"__metricName__": "metric_one"},
            {"__metricName__": "metric_one"},
            {"__metricName__": "metric_one"},
            {"__metricName__": "metric_one"},
            {"__severity__": "HIGH"},
        ]
        target = [
            {},
            {},
            {"__metricName__": "metric_two"},
            {"__metricName__": "metric_two"},
            {"__metricName__": "metric_two"},
            {"__metricName__": "metric_two"},
            {"__metricName__": "metric_two"},
            {},
            {"__severity__": "LOW"}
        ]
        equals = [
            [],
            [],
            [],
            [],
            [],
            ["hostname"],
            ["hostname"],
            ["hostname"],
            ["__alarmName__"]
        ]
        exclusions = [
            {},
            {},
            {},
            {},
            {"__metricName__": "metric_three"},
            {"__metricName__": "metric_three"},
            {},
            {},
            {"__alarmName__": "alarm_one"}
        ]
        for i in range(len(expressions)):
            test_source, test_target, test_equals, test_exclusions = \
                aql_parser.parse_inhibit_expression(expressions[i])
            self.assertEqual(test_source, source[i])
            self.assertEqual(test_target, target[i])
            self.assertEqual(test_equals, equals[i])
            self.assertEqual(test_exclusions, exclusions[i])

        for i in range(len(negative_expressions)):
            self.assertRaises(query_structures.QueryException,
                              aql_parser.parse_inhibit_expression,
                              negative_expressions[i])

    def test_parse_silence_rule(self):
        expressions = [
            "",
            "targets metric_one",
            "targets metric_one{}",
            "targets metric_one{hostname=host_one}",
            "targets metric_one{hostname=host_one, region=region_one}",
        ]
        negative_expressions = [
            "excludes metric_one",
            "source metric_one",
            "group by hostname",
            "targets metric_one, {hostname=host_one}",
        ]
        matchers = [
            {},
            {"__metricName__": "metric_one"},
            {"__metricName__": "metric_one"},
            {"__metricName__": "metric_one", "hostname": "host_one"},
            {"__metricName__": "metric_one", "hostname": "host_one", "region": "region_one"},
        ]
        for i in range(len(expressions)):
            test_matchers = aql_parser.parse_silence_expression(expressions[i])
            self.assertEqual(test_matchers, matchers[i])

        for i in range(len(negative_expressions)):
            self.assertRaises(query_structures.QueryException,
                              aql_parser.parse_silence_expression,
                              negative_expressions[i])
