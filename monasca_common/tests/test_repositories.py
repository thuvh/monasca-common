# Copyright (c) 2016 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
import unittest

import monasca_common.repositories.exceptions as exceptions
from monasca_common.repositories.mysql import mysql_repository


class TestMySQLRepository(unittest.TestCase):

    def setUp(self):
        self.log_patcher = mock.patch(
            'monasca_common.repositories.mysql.mysql_repository.LOG')
        self.cfg_patcher = mock.patch(
            'monasca_common.repositories.mysql.mysql_repository.cfg')
        self.mdb_patcher = mock.patch(
            'monasca_common.repositories.mysql.mysql_repository.mdb')

        self.mock_log = self.log_patcher.start()
        self.mock_cfg = self.cfg_patcher.start()
        self.mock_mdb = self.mdb_patcher.start()

    def tearDown(self):
        self.log_patcher.stop()
        self.cfg_patcher.stop()
        self.mdb_patcher.start()

    def test_init(self):
        mysql_repository_obj = mysql_repository.MySQLRepository()

        self.assertEqual(mysql_repository_obj.conf, self.mock_cfg.CONF)
        self.assertEqual(mysql_repository_obj.database_name,
                         self.mock_cfg.CONF.mysql.database_name)
        self.assertEqual(mysql_repository_obj.database_server,
                         self.mock_cfg.CONF.mysql.hostname)
        self.assertEqual(mysql_repository_obj.database_uid,
                         self.mock_cfg.CONF.mysql.username)
        self.assertEqual(mysql_repository_obj.database_pwd,
                         self.mock_cfg.CONF.mysql.password)

    def test_init_with_exception(self):
        self.mock_cfg.CONF = None

        self.assertRaises(exceptions.RepositoryException,
                          mysql_repository.MySQLRepository)

    def test_execute_query(self):
        query = mock.Mock()
        params = mock.Mock()
        ctx = self.mock_mdb.connect.return_value
        cursor = ctx.cursor.return_value
        mysql_repository_obj = mysql_repository.MySQLRepository()

        mysql_repository_obj._execute_query(query, params)

        self.assertTrue(self.mock_mdb.connect.called)
        ctx.cursor.assert_called_once_with(self.mock_mdb.cursors.DictCursor)
        cursor.execute.assert_called_once_with(query, params)
        self.assertTrue(cursor.fetchall)

    def _test_mysql_try_catch_block_decorator_with_exception(
            self, exception, expected_exception=None):
        @mysql_repository.mysql_try_catch_block
        def raise_exception():
            raise exception

        if expected_exception is None:
            expected_exception = exception

        self.assertRaises(expected_exception.__class__, raise_exception)

    def test_mysql_try_catch_decorator_with_repository_exceptions(self):
        for exception in [exceptions.DoesNotExistException(),
                          exceptions.AlreadyExistsException(),
                          exceptions.InvalidUpdateException()]:
            self._test_mysql_try_catch_block_decorator_with_exception(
                exception)

    def test_mysql_try_catch_decorator_with_non_repository_exception(self):
        class NonRepositoryException(Exception):
            pass
        exception = NonRepositoryException()

        self._test_mysql_try_catch_block_decorator_with_exception(
            exception,
            expected_exception=exceptions.RepositoryException(exception))
        self.mock_log.exception.assert_called_once_with(
            exception)
