"""Test ``auth`` module."""

from unittest import TestCase


class TestAuthorizationPolicy(TestCase):

    def make_one(self):
        from poulda.auth import AuthorizationPolicy
        return AuthorizationPolicy()

    def test_principals_allowed_by_permission(self):
        policy = self.make_one()
        args = 'context', 'permission'
        self.assertRaises(NotImplementedError,
                          policy.principals_allowed_by_permission, *args)

    def test_permits(self):
        from pyramid.security import Authenticated
        from poulda.auth import PERMISSION_UPLOAD
        permission = PERMISSION_UPLOAD
        context = 'context is ignored'
        policy = self.make_one()
        self.assert_(not policy.permits(context, [], permission))
        self.assert_(policy.permits(context, [Authenticated], permission))

    def test_permits_rejects_unknown_permission(self):
        policy = self.make_one()
        args = ('context is ignored', (), 'unknown permission')
        self.assertRaises(ValueError, policy.permits, *args)
