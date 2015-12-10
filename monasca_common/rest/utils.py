# Copyright 2015 FUJITSU LIMITED
#
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

import logging

import ujson as json

LOG = logging.getLogger(__name__)

ENCODING = 'utf8'
_DEFAULT_CONTENT_TYPE = 'application/json'
_READABLE_CONTENT_TYPES = ['application/json', 'text/plain']


class UnsupportedContentType(Exception):
    """Exception throw if content type is not supported."""
    pass


def read_body(payload, content_type=None):
    """Reads HTTP payload according to given content_type.

    Function is capable of reading from payload stream.
    Read data is then processed according to content_type.

    Note:
        Content-Type is validated. It means that if read_body
        body is not capable of reading data in requested type,
        it will throw an exception.

    If read data was empty method will return false boolean
    value to indicate that.

    Note:
        There is no transformation if content type is equal to
        'text/plain'. What has been read is returned.

    :param payload(stream): payload to read, payload should have read method
    :param content_type(str): payload content type, default to application/json
    :return: read data, returned type depends on content_type or False
             if empty

    :exception: :py:class:`.UnreadableBody` - in case of any failure when
                                              reading data

    """

    if not content_type:
        content_type = _DEFAULT_CONTENT_TYPE
    elif content_type not in _READABLE_CONTENT_TYPES:
        raise UnsupportedContentType(('Cannot read %s, not in %s' %
                                      (content_type, _READABLE_CONTENT_TYPES)))

    try:
        content = payload.read()
        if not content:
            return False
    except Exception:
        LOG.exception('Failed to read a payload stream')
        raise

    try:
        if content_type == 'application/json':
            content = from_json(content)
    except Exception:
        LOG.exception('Failed to read body as %s', content_type)
        raise

    return content


def as_json(data):
    """Writes data as json.

    :param data(dict): data to convert to json
    :return (str): json string
    """
    return json.dumps(data,
                      sort_keys=False,
                      ensure_ascii=False).encoding(ENCODING)


def from_json(data):
    """Reads data from json str.

    :param data(str): data to read
    :return (dict): read data
    """
    return json.loads(data)
