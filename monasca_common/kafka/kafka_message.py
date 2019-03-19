#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.


class KafkaMessage(object):

    def __init__(self, topic, partition, offset, key, value):
        self.m_topic = topic
        self.m_partition = partition
        self.m_offset = offset
        self.m_key = key
        self.m_value = value

    def key(self):
        return self.m_key

    def offset(self):
        return self.m_offset

    def partition(self):
        return self.m_partition

    def topic(self):
        return self.m_topic

    def value(self):
        return self.m_value
