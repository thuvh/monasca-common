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

import json
import logging
import re

log = logging.getLogger(__name__)

# This is used to ensure that metrics with a timestamp older than
# RECENT_POINT_THRESHOLD_DEFAULT seconds (or the value passed in to
# the MetricsAggregator constructor) get discarded rather than being
# input into the incorrect bucket. Currently, the MetricsAggregator
# does not support submitting values for the past, and all values get
# submitted for the timestamp passed into the flush() function.
RECENT_POINT_THRESHOLD_DEFAULT = 3600
VALUE_META_MAX_NUMBER = 16
VALUE_META_VALUE_MAX_LENGTH = 2048
VALUE_META_NAME_MAX_LENGTH = 255

invalid_chars = "<>={}(),\"\\\\;&"
restricted_dimension_chars = re.compile('[' + invalid_chars + ']')
restricted_name_chars = re.compile('[' + invalid_chars + ' ' + ']')


class InvalidMetricName(Exception):
    pass


class InvalidDimensionKey(Exception):
    pass


class InvalidDimensionValue(Exception):
    pass


class InvalidValue(Exception):
    pass


class InvalidValueMeta(Exception):
    pass


def metric_value_meta(value_meta):
    if len(value_meta) > VALUE_META_MAX_NUMBER:
        msg = "Too many valueMeta entries {0}, limit is {1}: valueMeta {2}"
        log.error(msg.format(len(value_meta), VALUE_META_MAX_NUMBER,
                             value_meta))
        raise InvalidValueMeta
    for key, value in value_meta.iteritems():
        if not key:
            log.error("valueMeta name cannot be empty")
            raise InvalidValueMeta
        if len(key) > VALUE_META_NAME_MAX_LENGTH:
            msg = "valueMeta name {0} must be {1} characters or less"
            log.error(msg.format(key, VALUE_META_NAME_MAX_LENGTH))
            raise InvalidValueMeta

    try:
        value_meta_json = json.dumps(value_meta)
        if len(value_meta_json) > VALUE_META_VALUE_MAX_LENGTH:
            msg = "valueMeta name value combinations must be {0} characters " \
                  "or less: valueMeta {1}"
            log.error(msg.format(VALUE_META_VALUE_MAX_LENGTH, value_meta))
            raise InvalidValueMeta
    except Exception:
            log.error("Unable to serialize valueMeta into JSON")
            raise InvalidValueMeta


def metric_dimensions(dimensions):
    for k, v in dimensions.iteritems():
        if not isinstance(k, (str, unicode)):
            log.error("invalid dimension key {0} must be a string: {1}".
                      format(k, dimensions))
            raise InvalidDimensionKey
        if len(k) > 255 or len(k) < 1:
            log.error("invalid length for dimension key {0}: {1}".
                      format(k, dimensions))
            raise InvalidDimensionKey
        if restricted_dimension_chars.search(k) or re.match('^_', k):
            log.error("invalid characters in dimension key {0}: {1}".
                      format(k, dimensions))
            raise InvalidDimensionKey

        if not isinstance(v, (str, unicode)):
            log.error("invalid dimension value {0} for key {1} must be a "
                      "string: {2}".format(v, k, dimensions))
            raise InvalidDimensionValue
        if len(v) > 255 or len(v) < 1:
            log.error("invalid length dimension value {0} for key {1}: {"
                      "2}".format(v, k, dimensions))
            raise InvalidDimensionValue
        if restricted_dimension_chars.search(v):
            log.error("invalid characters in dimension value {0} for key {1}: "
                      "{2}".format(v, k, dimensions))
            raise InvalidDimensionValue


def metric_name(name):
    if not isinstance(name, (str, unicode)):
        log.error("invalid metric name must be a string: {0} ".format(name))
        raise InvalidMetricName
    if len(name) > 255 or len(name) < 1:
        log.error("invalid length for metric name: {0}".format(name))
        raise InvalidMetricName
    if restricted_name_chars.search(name):
        log.error("invalid characters in metric name: {0}".format(name))
        raise InvalidMetricName


def metric_value(value):
    if not isinstance(value, (int, long, float)):
        log.error("invalid value {0} is not of number type for metric".format(
            value))
        raise InvalidValue
