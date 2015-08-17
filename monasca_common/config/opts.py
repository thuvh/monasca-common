# Copyright (c) 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from oslo_config import cfg


logging_opts = [
    cfg.StrOpt('level', default='INFO'),
    cfg.StrOpt('file', default='/var/log/monasca/events/events_engine.log'),
    cfg.StrOpt('size', default=10485760),
    cfg.StrOpt('backup', default=5),
    cfg.StrOpt('kazoo', default="WARN"),
    cfg.StrOpt('kafka', default="WARN"),
    cfg.StrOpt('iso8601', default="WARN"),
    cfg.StrOpt('statsd', default="WARN")]
logging_group = cfg.OptGroup(name='logging', title='logging')

mysql_opts = [
    cfg.StrOpt('database_name'),
    cfg.StrOpt('hostname'),
    cfg.StrOpt('username'),
    cfg.StrOpt('password')]
mysql_group = cfg.OptGroup(name='mysql', title='mysql')

kafka_opts = [
    cfg.StrOpt('url', help='The address to the kafka server. '
               'For example: url=192.168.10.4:9092'),
    cfg.StrOpt('events_topic', default='raw-events',
               help='The topic that events will be read from.'),
    cfg.StrOpt('event_group', default='monasca-event',
               help='The group name for reading events.'),
    cfg.StrOpt('stream_def_topic', default='stream-definitions',
               help='The topic for stream definition events.'),
    cfg.StrOpt('stream_def_group', default='streams_1',
               help='The event processor '
               'group for stream defs for this server'),
    cfg.StrOpt('stream_def_pipe_group', default='streams_pipe_1',
               help='The group for stream defs for this server'),
    cfg.StrOpt('notifications_topic', default='stream-notifications',
               help='The topic for sending notification events.'),
    cfg.StrOpt('transformed_events_topic', default='transformed-events',
               help='The topic for reading transformed events.'),
    cfg.StrOpt('transform_group', default='monasca-event',
               help='The group name for reading raw events.'),
    cfg.StrOpt('transform_def_topic', default='transform-definitions',
               help='The topic for transform definition events.'),
    cfg.IntOpt('fetch_size', default=32768,
               help='The number of fetch size bytes.'),
    cfg.IntOpt('buffer_size', default=32768, help='The buffer size.'),
    cfg.IntOpt('max_buffer_size', default=262144,
               help='Recommended 8 times the buffer size.')]
kafka_group = cfg.OptGroup(name='kafka', title='kafka')

zookeeper_opts = [
    cfg.StrOpt('url', help='The address to the zookeeper server. '
               'For example:  url=192.168.10.4:2181')]
zookeeper_group = cfg.OptGroup(name='zookeeper', title='zookeeper')
