# Copyright 2017 OP5 AB
# Copyright 2011 Piston Cloud Computing, Inc.
# All Rights Reserved.

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
import requests_mock

from oslo_context import context
from oslo_policy import policy as os_policy
from testfixtures import TempDirectory

from monasca_common.policy_engine import policy
from monasca_common.tests.policy import base


class PolicyFileTestCase(base.BaseTestCase):
    def setUp(self):
        super(PolicyFileTestCase, self).setUp()
        self.context = context.RequestContext(user='fake',
                                              tenant='fake',
                                              is_admin=False)
        self.target = {}

    def test_modified_policy_reloads(self):

        with TempDirectory() as policy_dir:
            policy_dir.write('policy.yaml', '{}')

            base.BaseTestCase.conf_override(policy_file='{0}/policy.yaml'.format(policy_dir.path),
                                       group='oslo_policy')
            policy.reset()
            policy.init()

            action = 'example:test'
            rule = os_policy.RuleDefault(action, '')

            policy._ENFORCER.register_defaults([rule])

            policy_dir.write('policy.yaml', '{"example:test": ""}')

            policy.authorize(self.context, action, self.target)

            policy_dir.write('policy.yaml', '{"example:test": "!"}')
            policy._ENFORCER.load_rules(True)

            self.assertRaises(os_policy.PolicyNotAuthorized, policy.authorize,
                              self.context, action, self.target)


class PolicyTestCase(base.BaseTestCase):
    def setUp(self):
        super(PolicyTestCase, self).setUp()
        rules = [
            os_policy.RuleDefault("true", "@"),
            os_policy.RuleDefault("example:allowed", "@"),
            os_policy.RuleDefault("example:denied", "!"),
            os_policy.RuleDefault("old_action_not_default", "@"),
            os_policy.RuleDefault("new_action", "@"),
            os_policy.RuleDefault("old_action_default", "rule:admin_api"),
            os_policy.RuleDefault("example:lowercase_admin",
                                  "role:admin or role:sysadmin"),
            os_policy.RuleDefault("example:uppercase_admin",
                                  "role:ADMIN or role:sysadmin"),
            os_policy.RuleDefault("example:get_http",
                                    "http://www.example.com"),
            os_policy.RuleDefault("example:my_file",
                                  "role:compute_admin or "
                                  "project_id:%(project_id)s"),
            os_policy.RuleDefault("example:early_and_fail", "! and @"),
            os_policy.RuleDefault("example:early_or_success", "@ or !"),
        ]
        policy.reset()
        policy.init()

        self.context = context.RequestContext(user='fake',
                                              tenant='fake',
                                              is_admin=False)
        policy._ENFORCER.register_defaults(rules)
        self.target = {}

    def test_authorize_nonexistent_action_throws(self):

        action = 'example:noexists'
        self.assertRaises(os_policy.PolicyNotRegistered, policy.authorize,
                          self.context, action, self.target)

    def test_authorize_bad_action_throws(self):
        action = 'example:denied'
        self.assertRaises(os_policy.PolicyNotAuthorized, policy.authorize,
                          self.context, action, self.target)

    def test_authorize_bad_action_noraise(self):
        action = "example:denied"
        result = policy.authorize(self.context, action, self.target, False)
        self.assertFalse(result)

    def test_authorize_good_action(self):
        action = "example:allowed"
        result = policy.authorize(self.context, action, self.target)
        self.assertTrue(result)

    @requests_mock.mock()
    def test_authorize_http_true(self, req_mock):
        req_mock.post('http://www.example.com/',
                      text='True')
        action = "example:get_http"
        target = {}
        result = policy.authorize(self.context, action, target)
        self.assertTrue(result)

    @requests_mock.mock()
    def test_authorize_http_false(self, req_mock):
        req_mock.post('http://www.example.com/',
                      text='False')
        action = "example:get_http"
        target = {}
        self.assertRaises(os_policy.PolicyNotAuthorized, policy.authorize,
                          self.context, action, target)

    def test_templatized_authorization(self):
        target_mine = {'project_id': 'fake'}
        target_not_mine = {'project_id': 'another'}
        action = "example:my_file"
        policy.authorize(self.context, action, target_mine)
        self.assertRaises(os_policy.PolicyNotAuthorized, policy.authorize,
                          self.context, action, target_not_mine)

    def test_early_AND_authorization(self):
        action = "example:early_and_fail"
        self.assertRaises(os_policy.PolicyNotAuthorized, policy.authorize,
                          self.context, action, self.target)

    def test_early_OR_authorization(self):
        action = "example:early_or_success"
        policy.authorize(self.context, action, self.target)

    def test_ignore_case_role_check(self):
        lowercase_action = "example:lowercase_admin"
        uppercase_action = "example:uppercase_admin"
        # NOTE(dprince) we mix case in the Admin role here to ensure
        # case is ignored
        admin_context = context.RequestContext('admin',
                                               'fake',
                                               roles=['AdMiN'])
        policy.authorize(admin_context, lowercase_action, self.target)
        policy.authorize(admin_context, uppercase_action, self.target)

    @mock.patch.object(policy.LOG, 'warning')
    def test_warning_when_deprecated_user_based_rule_used(self, mock_warning):
        policy._warning_for_deprecated_user_based_rules(
            [("os_compute_api:servers:index",
              "project_id:%(project_id)s or user_id:%(user_id)s")])
        mock_warning.assert_called_once_with(
            u"The user_id attribute isn't supported in the rule "
            "'%s'. All the user_id based policy enforcement will be removed "
            "in the future.", "os_compute_api:servers:index")

    @mock.patch.object(policy.LOG, 'warning')
    def test_no_warning_for_user_based_resource(self, mock_warning):
        policy._warning_for_deprecated_user_based_rules(
            [("os_compute_api:os-keypairs:index",
              "user_id:%(user_id)s")])
        mock_warning.assert_not_called()

    @mock.patch.object(policy.LOG, 'warning')
    def test_no_warning_for_no_user_based_rule(self, mock_warning):
        policy._warning_for_deprecated_user_based_rules(
            [("os_compute_api:servers:index",
              "project_id:%(project_id)s")])
        mock_warning.assert_not_called()

    @mock.patch.object(policy.LOG, 'warning')
    def test_verify_deprecated_policy_using_old_action(self, mock_warning):
        policy._ENFORCER.load_rules(True)
        old_policy = "old_action_not_default"
        new_policy = "new_action"
        default_rule = "rule:admin_api"

        using_old_action = policy.verify_deprecated_policy(
            old_policy, new_policy, default_rule, self.context)

        mock_warning.assert_called_once_with("Start using the new "
                                             "action '{0}'. The existing action '{1}' is being deprecated and "
                                             "will be removed in future release.".format(new_policy,
                                                                                         old_policy))
        self.assertTrue(using_old_action)

    def test_verify_deprecated_policy_using_new_action(self):
        policy._ENFORCER.load_rules(True)
        old_policy = "old_action_default"
        new_policy = "new_action"
        default_rule = "rule:admin_api"

        using_old_action = policy.verify_deprecated_policy(
            old_policy, new_policy, default_rule, self.context)

        self.assertFalse(using_old_action)


class IsAdminCheckTestCase(base.BaseTestCase):
    def setUp(self):
        super(IsAdminCheckTestCase, self).setUp()
        policy.init()

    def test_init_true(self):
        check = policy.IsAdminCheck('is_admin', 'True')

        self.assertEqual(check.kind, 'is_admin')
        self.assertEqual(check.match, 'True')
        self.assertTrue(check.expected)

    def test_init_false(self):
        check = policy.IsAdminCheck('is_admin', 'nottrue')

        self.assertEqual(check.kind, 'is_admin')
        self.assertEqual(check.match, 'False')
        self.assertFalse(check.expected)

    def test_call_true(self):
        check = policy.IsAdminCheck('is_admin', 'True')

        self.assertTrue(check('target', dict(is_admin=True),
                              policy._ENFORCER))
        self.assertFalse(check('target', dict(is_admin=False),
                               policy._ENFORCER))

    def test_call_false(self):
        check = policy.IsAdminCheck('is_admin', 'False')

        self.assertFalse(check('target', dict(is_admin=True),
                               policy._ENFORCER))
        self.assertTrue(check('target', dict(is_admin=False),
                              policy._ENFORCER))


class AdminRolePolicyTestCase(base.BaseTestCase):
    def setUp(self):
        super(AdminRolePolicyTestCase, self).setUp()
        self.noadmin_context = context.RequestContext('fake', 'fake', roles=['member'])
        self.admin_context = context.RequestContext('fake', 'fake', roles=['admin'])

        admin_rule = [
            os_policy.RuleDefault('example.admin', 'role:admin'),
        ]
        policy.reset()
        policy.init(policy_file=None)
        policy._ENFORCER.register_defaults(admin_rule)
        policy._ENFORCER.load_rules(True)
        self.target = {}

    def test_authorize_admin_actions_with_admin_context(self):
        for action in policy.get_rules().keys():
            policy.authorize(self.admin_context, action, self.target)

    def test_authorize_admin_actions_with_nonadmin_context_throws(self):
        """Check if non-admin context passed to admin actions throws
           Policy not authorized exception
        """
        for action in policy.get_rules().keys():
            self.assertRaises(os_policy.PolicyNotAuthorized, policy.authorize,
                          self.noadmin_context, action, self.target)
