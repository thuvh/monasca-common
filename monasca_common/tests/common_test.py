# Copyright (c) 2015 Hewlett-Packard Development Company, L.P.
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
import os
import tempfile
import unittest

from oslo_config import cfg

from monasca_common.config import register
from monasca_common.logging import dict_config


class CommonTests(unittest.TestCase):

    def test_logging_config(self):
        tempfile_path = tempfile.mkstemp()[1]
        try:
            outfile = open(tempfile_path, 'w')
            outfile.writelines(
                ['[logging]\n', 'level = DEBUG\n', 'backup = 3\n'])
            outfile.close()

            cfg.CONF(args=[], project='test',
                     default_config_files=[tempfile_path])
            register.register_logging_opts(cfg.CONF)
            log_config = dict_config.get_config(cfg.CONF)
        finally:
            os.remove(tempfile_path)
        self.assertEqual(log_config['handlers']['file']['backupCount'], str(3))
