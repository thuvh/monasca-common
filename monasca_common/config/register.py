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
from monasca_common.config import opts


def register_logging_opts(conf):
    conf.register_group(opts.logging_group)
    conf.register_opts(opts.logging_opts, opts.logging_group)


def register_mysql_opts(conf):
    conf.register_group(opts.mysql_group)
    conf.register_opts(opts.mysql_opts, opts.mysql_group)


def register_kafka_opts(conf):
    conf.register_group(opts.kafka_group)
    conf.register_opts(opts.kafka_opts, opts.kafka_group)


def register_zookeeper_opts(conf):
    conf.register_group(opts.zookeeper_group)
    conf.register_opts(opts.zookeeper_opts, opts.zookeeper_group)
