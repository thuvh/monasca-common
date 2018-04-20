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

import datetime

import falcon
from oslo_log import log
from oslo_utils import timeutils
import six
import ujson as json

from monasca_common.rest import exceptions
from monasca_common.validation import metrics as metric_validation

LOG = log.getLogger(__name__)

ENCODING = 'utf8'

TEXT_CONTENT_TYPE = 'text/plain'
JSON_CONTENT_TYPE = 'application/json'


def _try_catch(fun):

    @six.wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except Exception as ex:
            raise exceptions.DataConversionException(str(ex))

    return wrapper


@_try_catch
def as_json(data, **kwargs):
    """Writes data as json.

    :param dict data: data to convert to json
    :param kwargs kwargs: kwargs for json dumps
    :return: json string
    :rtype: str
    """

    if 'sort_keys' not in kwargs:
        kwargs['sort_keys'] = False
    if 'ensure_ascii' not in kwargs:
        kwargs['ensure_ascii'] = False

    data = json.dumps(data, **kwargs)

    return data


@_try_catch
def from_json(data, **kwargs):
    """Reads data from json str.

    :param str data: data to read
    :param kwargs kwargs: kwargs for json loads
    :return: read data
    :rtype: dict
    """
    return json.loads(data, **kwargs)


_READABLE_CONTENT_TYPES = {
    TEXT_CONTENT_TYPE: lambda content: content,
    JSON_CONTENT_TYPE: from_json
}


def read_body(payload, content_type=JSON_CONTENT_TYPE):
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

    :param stream payload: payload to read, payload should have read method
    :param str content_type: payload content type, default to application/json
    :return: read data, returned type depends on content_type or False
             if empty

    :exception: :py:class:`.UnreadableBody` - in case of any failure when
                                              reading data

    """
    if content_type not in _READABLE_CONTENT_TYPES:
        msg = ('Cannot read %s, not in %s' %
               (content_type, _READABLE_CONTENT_TYPES))
        raise exceptions.UnsupportedContentTypeException(msg)

    try:
        content = payload.read()
        if not content:
            return None
    except Exception as ex:
        raise exceptions.UnreadableContentError(str(ex))

    return _READABLE_CONTENT_TYPES[content_type](content)


def validate_authorization(req, authorized_roles):
    """Validates whether one or more X-ROLES in the HTTP header is authorized.

    If authorization fails, 401 is thrown with appropriate description.
    Additionally response specifies 'WWW-Authenticate' header with 'Token'
    value challenging the client to use different token (the one with
    different set of roles).

    :param req: HTTP request object. Must contain "X-ROLES" in the HTTP
                request header.
    :param authorized_roles: List of authorized roles to check against.

    :raises falcon.HTTPUnauthorized
    """
    roles = req.roles
    challenge = 'Token'
    if not roles:
        raise falcon.HTTPUnauthorized('Forbidden',
                                      'Tenant does not have any roles',
                                      challenge)
    roles = roles.split(',') if isinstance(roles, six.string_types) else roles
    authorized_roles_lower = [r.lower() for r in authorized_roles]
    for role in roles:
        role = role.lower()
        if role in authorized_roles_lower:
            return
    raise falcon.HTTPUnauthorized('Forbidden',
                                  'Tenant ID is missing a required role to '
                                  'access this service',
                                  challenge)


def get_x_tenant_or_tenant_id(req, delegate_authorized_roles):
    """Evaluates whether the tenant ID or cross tenant ID should be returned.

    For example, a service with openstack credentials from project X may post
    to the monasca-apis on behalf of openstack project Y, if the user in
    project X has a delegate role.

    :param req: HTTP request object.
    :param delegate_authorized_roles: List of authorized roles that have
                                      delegate privileges.

    :returns: Returns the cross tenant or tenant ID.
    """
    if any(x in set(delegate_authorized_roles) for x in req.roles):
        params = falcon.uri.parse_query_string(req.query_string)
        if 'tenant_id' in params:
            tenant_id = params['tenant_id']
            return tenant_id
    return req.project_id


def get_query_param(param):
    try:
        if isinstance(param, list):
            param_val = param[0].decode(ENCODING)
        else:
            param_val = param.decode(ENCODING)
        return param_val
    except Exception as ex:
        LOG.debug(ex)
        raise exceptions.HTTPUnprocessableEntityError('Unprocessable Entity', str(ex))


def get_query_dimensions(dimensions_param):
    """Parses the query dimensions parameter.

    :param dimensions_param: Raw dimensions extracted from HTTP request body
    :return: Dimensions as a JSON object
    :raises falcon.HTTPUnprocessableEntity: If dimensions are malformed.
    """
    try:
        dimensions = {}
        if not dimensions_param:
            return dimensions
        elif isinstance(dimensions_param, six.string_types):
            dimensions_str_array = dimensions_param.split(',')
        elif isinstance(dimensions_param, list):
            dimensions_str_array = []
            for sublist in dimensions_param:
                dimensions_str_array.extend(sublist.split(","))
        else:
            raise Exception("Error parsing dimensions, unknown format")

        for dimension in dimensions_str_array:
            dimension_name_value = dimension.split(':', 1)
            if len(dimension_name_value) == 2:
                dimensions[dimension_name_value[0]] = dimension_name_value[1]
            elif len(dimension_name_value) == 1:
                dimensions[dimension_name_value[0]] = ""
        return dimensions
    except Exception as ex:
        LOG.debug(ex)
        raise exceptions.HTTPUnprocessableEntityError('Unprocessable Entity', str(ex))


def _convert_time_string(date_time_string):
    dt = timeutils.parse_isotime(date_time_string)
    dt = timeutils.normalize_time(dt)
    timestamp = (dt - datetime.datetime(1970, 1, 1)).total_seconds()
    return timestamp


def get_query_timestamp(time):
    try:
        return _convert_time_string(time)
    except Exception as ex:
        LOG.debug(ex)
        raise exceptions.HTTPUnprocessableEntityError('Unprocessable Entity', str(ex))


def validate_timestamp_order(start_timestamp, end_timestamp):
    if start_timestamp and end_timestamp:
        if not start_timestamp < end_timestamp:
            raise exceptions.HTTPUnprocessableEntityError(
                'Invalid time ordering:', 'start_time must be before end_time')


def validate_query_dimensions(dimensions):
    """Validates the query param dimensions.

    :param dimensions: Raw dimensions.
    :return: Dimensions as a list of tuples.
    :raises falcon.HTTPUnprocessableEntity: If dimensions are malformed.
    """
    try:
        result = {}
        for key, value in dimensions.items():
            # TODO(dszumski): We need more validation here
            if key.startswith('_'):
                raise Exception("Dimension key {} may not start with '_'".format(key))
            metric_validation.validate_dimension_key(key)
            values = None
            if value:
                if '|' in value:
                    values = value.split('|')
                    for v in values:
                        metric_validation.validate_dimension_value(key, v)
                else:
                    metric_validation.validate_dimension_value(key, value)
                    values = [value]
            result[key] = values
        return result
    except Exception as ex:
        LOG.debug(ex)
        raise exceptions.HTTPUnprocessableEntityError('Unprocessable Entity', str(ex))
