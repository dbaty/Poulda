"""Define the authentication and authorization policies."""

from pyramid.security import Authenticated


PERMISSION_UPLOAD = u'upload'


class AuthorizationPolicy(object):
    """A simple authorization policy that states that any
    authenticated user is granted the 'upload' permission (and that
    this is the only known permission).
    """

    def principals_allowed_by_permission(self, context, permission):
        raise NotImplementedError

    def permits(self, context, principals, permission):
        # There is only one permission: 'upload'.
        if permission != PERMISSION_UPLOAD:
            raise ValueError('Unexpected permission: "%s"' % permission)
        # All authenticated users are granted the 'upload' permission.
        return Authenticated in principals
